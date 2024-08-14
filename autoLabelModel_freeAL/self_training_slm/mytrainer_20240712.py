from transformers import AutoConfig, AutoModelForSequenceClassification, Trainer, HfArgumentParser, set_seed
from transformers.trainer import *
import torch
from torch import nn
import os
import copy
from torch.utils.data import DataLoader
import numpy as np
import torch.nn.functional as F
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union
from torch.nn import CrossEntropyLoss, KLDivLoss, NLLLoss, BCEWithLogitsLoss
from sklearn.metrics import confusion_matrix, recall_score, roc_auc_score, accuracy_score, f1_score
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 线性热身批次 从小到大 ，比如 1/10 2/10 3/10 ...10/10 结束
def linear_rampup(current, rampup_length):
    """Linear rampup"""
    assert current >= 0 and rampup_length >= 0
    if current >= rampup_length:
        return 1.0
    else:
        return current / rampup_length


# 1.训练器（SLM训练核心代码）
class MyTrainer(Trainer):
    # 1.1 内部训练循环,包含外围方法 1.train（）之内
    def _inner_training_loop(self, batch_size=None, args=None, resume_from_checkpoint=None, trial=None,
                             ignore_keys_for_eval=None):
        # 每个batch的大小
        self._train_batch_size = batch_size
        # 1. 训练参数和数据集设置 ：Data loader and number of training steps
        # 训练数据的dataloader
        train_dataloader = self.get_train_dataloader()

        # 设置训练控制变量 Setting up training control variables:
        # number of training epochs: num_train_epochs 训练epoch次数
        # number of training steps per epoch: num_update_steps_per_epoch 每个epoch的更新的步数
        # total number of training steps to execute: max_steps 整体的最大的训练步数
        # 整体的并行的训练容量= batch*batch中梯度更新需要几个steo*词的向量大小
        total_train_batch_size = args.train_batch_size * args.gradient_accumulation_steps * args.world_size

        len_dataloader = None
        if has_length(train_dataloader):  # 训练数据集如果有数据
            len_dataloader = len(train_dataloader)  # 训练数据的长度
            # num_update_steps_per_epoch：每个epoch的更新步数：每个迭代总数据/每个batch梯度步次，除法向下取整，
            # https://zhuanlan.zhihu.com/p/353743194
            num_update_steps_per_epoch = len_dataloader // args.gradient_accumulation_steps
            num_update_steps_per_epoch = max(num_update_steps_per_epoch, 1)  # 至少比1大
            # 获取数据集样本数量
            num_examples = self.num_examples(train_dataloader)
            if args.max_steps > 0:  # 如果设置了max_steps的值
                max_steps = args.max_steps  # 最大步数
                #  训练的epoch总数 =最大步数/每个epoch的更新步数 除不尽则再+1
                num_train_epochs = args.max_steps // num_update_steps_per_epoch + int(
                    args.max_steps % num_update_steps_per_epoch > 0
                )
                # 训练样本数总数：最大步长*整体的并行的训练容量
                num_train_samples = args.max_steps * total_train_batch_size
            else:  # 没有设置max_steps，走num_train_epochs
                # max_steps:向上取整数(训练的epochs的值*每个epoch的更新步数)
                max_steps = math.ceil(args.num_train_epochs * num_update_steps_per_epoch)
                # 总的训练epoch数
                num_train_epochs = math.ceil(args.num_train_epochs)
                # 训练样本数总数：数据量*训练epochs
                num_train_samples = self.num_examples(train_dataloader) * args.num_train_epochs
        elif args.max_steps > 0:  # 训练数据没有设置working size。Rely on max_steps when dataloader does not have a working size
            max_steps = args.max_steps
            # 总的训练epoch数,设置很大的值:Setting a very large number of epochs so we go as many times as necessary over the iterator.
            num_train_epochs = sys.maxsize
            num_update_steps_per_epoch = max_steps
            # 样本数量= 整体的并行的训练容量*最大步长
            num_examples = total_train_batch_size * args.max_steps
            # 训练样本数总数：最大步长*整体的并行的训练容量
            num_train_samples = args.max_steps * total_train_batch_size
        else:
            raise ValueError(
                "args.max_steps must be set to a positive value if dataloader does not have a length, was"
                f" {args.max_steps}"
            )

        if DebugOption.UNDERFLOW_OVERFLOW in self.args.debug:
            if self.args.n_gpu > 1:
                # nn.DataParallel(model) replicates the model, creating new variables and module
                # references registered here no longer work on other gpus, breaking the module
                raise ValueError(
                    "Currently --debug underflow_overflow is not supported under DP. Please use DDP"
                    " (torch.distributed.launch)."
                )
            else:
                debug_overflow = DebugUnderflowOverflow(self.model)  # noqa

        # 2. 模型加载和优化器创建
        # 延时的优化器optimizer创建，ddp相关
        delay_optimizer_creation = (
                self.sharded_ddp is not None
                and self.sharded_ddp != ShardedDDPOption.SIMPLE
                or is_sagemaker_mp_enabled()
                or self.fsdp is not None
        )
        # 微软的大模型训练框架
        if args.deepspeed:
            deepspeed_engine, optimizer, lr_scheduler = deepspeed_init(
                self, num_training_steps=max_steps, resume_from_checkpoint=resume_from_checkpoint
            )
            self.model = deepspeed_engine.module
            self.model_wrapped = deepspeed_engine
            self.deepspeed = deepspeed_engine
            self.optimizer = optimizer
            self.lr_scheduler = lr_scheduler
        # 普通训练框架
        elif not delay_optimizer_creation:
            self.create_optimizer_and_scheduler(num_training_steps=max_steps)
        # 训练状态：模型和优化器分开
        self.state = TrainerState()
        self.state.is_hyper_param_search = trial is not None

        # Activate gradient checkpointing if needed 正向记录计算方法，反向的时候记录激活值https://zhuanlan.zhihu.com/p/689971296
        if args.gradient_checkpointing:
            self.model.gradient_checkpointing_enable()
        #  模型预热
        model = self._wrap_model(self.model_wrapped)

        if is_sagemaker_mp_enabled() and resume_from_checkpoint is not None:
            # 从checkpoint的地方恢复
            self._load_from_checkpoint(resume_from_checkpoint, model)

        # for the rest of this function `model` is the outside model, whether it was wrapped or not
        if model is not self.model:
            self.model_wrapped = model

        if delay_optimizer_creation:
            self.create_optimizer_and_scheduler(num_training_steps=max_steps)

        # Check if saved optimizer or scheduler states exist
        self._load_optimizer_and_scheduler(resume_from_checkpoint)

        # model是transformer的模型，model_wrapped是DDP等工具的模型。
        # important: at this point:
        # self.model         is the Transformers Model
        # self.model_wrapped is DDP(Transformers Model), Deepspeed(Transformers Model), etc.

        # 3.训练执行 Train! 展示设置和参数
        logger.info("***** Running training *****")
        logger.info(f"  Num examples = {num_examples}")
        logger.info(f"  Num Epochs = {num_train_epochs}")
        logger.info(f"  Instantaneous batch size per device = {args.per_device_train_batch_size}")
        logger.info(f"  Total train batch size (w. parallel, distributed & accumulation) = {total_train_batch_size}")
        logger.info(f"  Gradient Accumulation steps = {args.gradient_accumulation_steps}")
        logger.info(f"  Total optimization steps = {max_steps}")
        logger.info(
            f"  Number of trainable parameters = {sum(p.numel() for p in model.parameters() if p.requires_grad)}"
        )

        # 声明运行时变量：epoch，开始时间，已完成训练的epoches，当前epoch的steps值，step的进度条
        self.state.epoch = 0
        start_time = time.time()
        epochs_trained = 0
        steps_trained_in_current_epoch = 0
        steps_trained_progress_bar = None

        #  从checkpoint中恢复训练 Check if continuing training from a checkpoint
        if resume_from_checkpoint is not None and os.path.isfile(
                os.path.join(resume_from_checkpoint, TRAINER_STATE_NAME)
        ):
            # 从checkpoint加载模型
            self.state = TrainerState.load_from_json(os.path.join(resume_from_checkpoint, TRAINER_STATE_NAME))
            # 已完成的训练epoch：当前全局的step/每个epoch更新需要的steps
            epochs_trained = self.state.global_step // num_update_steps_per_epoch
            if not args.ignore_data_skip:
                # 当前epoch已完成的step
                steps_trained_in_current_epoch = self.state.global_step % (num_update_steps_per_epoch)
                # 当前epoch已完成的step*每个batch拆分的几个小step
                steps_trained_in_current_epoch *= args.gradient_accumulation_steps
            else:
                steps_trained_in_current_epoch = 0

            #  从checkpoint恢复训练，当前的epoch和挡墙的的总step
            logger.info("  Continuing training from checkpoint, will skip to saved global_step")
            logger.info(f"  Continuing training from epoch {epochs_trained}")
            logger.info(f"  Continuing training from global step {self.state.global_step}")
            if not args.ignore_data_skip:
                # 不跳过前面
                if skip_first_batches is None:
                    logger.info(
                        f"  Will skip the first {epochs_trained} epochs then the first"
                        f" {steps_trained_in_current_epoch} batches in the first epoch. If this takes a lot of time,"
                        " you can install the latest version of Accelerate with `pip install -U accelerate`.You can"
                        " also add the `--ignore_data_skip` flag to your launch command, but you will resume the"
                        " training on data already seen by your model."
                    )
                # 跳过前面的继续
                else:
                    logger.info(
                        f"  Will skip the first {epochs_trained} epochs then the first"
                        f" {steps_trained_in_current_epoch} batches in the first epoch."
                    )
                # 跳过first batches
                if self.is_local_process_zero() and not args.disable_tqdm and skip_first_batches is None:
                    steps_trained_progress_bar = tqdm(total=steps_trained_in_current_epoch)
                    steps_trained_progress_bar.set_description("Skipping the first batches")

        # 更新引用：模型、优化器、lr学习率计划、训练数据 Update the references
        self.callback_handler.model = self.model
        self.callback_handler.optimizer = self.optimizer
        self.callback_handler.lr_scheduler = self.lr_scheduler
        self.callback_handler.train_dataloader = train_dataloader
        #  hp_name(SigOpt/Optuna)
        if self.hp_name is not None and self._trial is not None:
            # use self._trial because the SigOpt/Optuna hpo only call `_hp_search_setup(trial)` instead of passing trial
            # parameter to Train when using DDP.
            self.state.trial_name = self.hp_name(self._trial)
        # trial (DDP)
        if trial is not None:
            assignments = trial.assignments if self.hp_search_backend == HPSearchBackend.SIGOPT else trial
            self.state.trial_params = hp_params(assignments)
        else:
            self.state.trial_params = None
        # This should be the same if the state has been saved but in case the training arguments changed, it's safer
        # to set this after the load.
        # 重新加载下state数据，以免有变。max_steps,训练的epoch数，
        self.state.max_steps = max_steps
        self.state.num_train_epochs = num_train_epochs
        self.state.is_local_process_zero = self.is_local_process_zero()
        self.state.is_world_process_zero = self.is_world_process_zero()

        # tr_loss loss的tensor，通过item()
        # tr_loss is a tensor to avoid synchronization of TPUs through .item()
        tr_loss = torch.tensor(0.0).to(args.device)
        # _total_loss_scalar 存储整体的loss，持续被更新
        # _total_loss_scalar is updated everytime .item() has to be called on tr_loss and stores the sum of all losses
        self._total_loss_scalar = 0.0
        self._globalstep_last_logged = self.state.global_step
        # 重置梯度
        model.zero_grad()
        # 开始训练（估计类似切面）
        self.control = self.callback_handler.on_train_begin(args, self.state, self.control)

        # 一些epoch设置
        # Skip the first epochs_trained epochs to get the random state of the dataloader at the right point.
        if not args.ignore_data_skip:
            for epoch in range(epochs_trained):
                is_random_sampler = hasattr(train_dataloader, "sampler") and isinstance(
                    train_dataloader.sampler, RandomSampler
                )
                if is_torch_less_than_1_11 or not is_random_sampler:
                    # We just need to begin an iteration to create the randomization of the sampler.
                    # That was before PyTorch 1.11 however...
                    for _ in train_dataloader:
                        break
                else:
                    # Otherwise we need to call the whooooole sampler cause there is some random operation added
                    # AT THE VERY END!
                    _ = list(train_dataloader.sampler)

        total_batched_samples = 0
        # 运行剩下的epoch（从当前epoch到最后一个poch）
        for epoch in range(epochs_trained, num_train_epochs):
            # 设epoch到数据集
            if isinstance(train_dataloader, DataLoader) and isinstance(train_dataloader.sampler, DistributedSampler):
                train_dataloader.sampler.set_epoch(epoch)
            elif hasattr(train_dataloader, "dataset") and isinstance(train_dataloader.dataset, IterableDatasetShard):
                train_dataloader.dataset.set_epoch(epoch)

            if is_torch_tpu_available():
                parallel_loader = pl.ParallelLoader(train_dataloader, [args.device]).per_device_loader(args.device)
                epoch_iterator = parallel_loader
            else:
                epoch_iterator = train_dataloader

            # 开始前 past值重置
            # Reset the past mems state at the beginning of each epoch if necessary.
            if args.past_index >= 0:
                self._past = None

            # 设置每个epoch中的实际step数
            steps_in_epoch = (
                len(epoch_iterator)
                if len_dataloader is not None
                else args.max_steps * args.gradient_accumulation_steps
            )

            # epoch开始的切面
            self.control = self.callback_handler.on_epoch_begin(args, self.state, self.control)

            # 如果有待恢复的checkpoint则恢复checkpoint
            if epoch == epochs_trained and resume_from_checkpoint is not None and steps_trained_in_current_epoch == 0:
                self._load_rng_state(resume_from_checkpoint)

            rng_to_sync = False
            steps_skipped = 0
            # 恢复之前训练过的step
            if skip_first_batches is not None and steps_trained_in_current_epoch > 0:
                epoch_iterator = skip_first_batches(epoch_iterator, steps_trained_in_current_epoch)
                steps_skipped = steps_trained_in_current_epoch
                steps_trained_in_current_epoch = 0
                rng_to_sync = True

            step = -1

            ##------------------------------------------------------------------

            # 3. 开始噪声学习样本选择和演示集构建
            ##Start of sample selection and demonstration pool construction
            # temp_u
            self.temp_u = args.temp_u
            # 获取数据量
            length = len(train_dataloader.dataset)
            # 选择列表：chosen_list 初始设置了数据长度的全0
            chosen_list = torch.zeros((length)).cuda()
            # 选择列表-选中的：先也是全0
            chosen_list_sel = torch.zeros((length)).cuda()
            # 标签类别数
            self.num_labels = args.num_labels
            # epoch大于1
            if epoch > 0:
                # 模型上到GPU上
                t_model = copy.deepcopy(model).to(args.device)
                # 先跑一轮
                t_model.eval()
                # 设置超参数rho_sel
                rho_sel = 0.2

                num_labels = args.num_labels  # 分类标签数
                targets_all = torch.zeros((length), dtype=torch.long).cuda()  # 初始化 target_all全0
                outputs_all = torch.zeros((length, num_labels)).cuda()  # 初始化 outputs_all全0 （输出结果标签）
                loss_all = torch.zeros((length)).cuda()  # 初始化 loss_all全0
                embeddings_all = torch.zeros((length, args.embedding_dim))  # 初始化 embeddings_all 全0，768向量
                new_dataloader = train_dataloader  # 训练数据
                # 3.1 计算训练样本之间的损失 Calculate the losses for each training sample
                for step, inputs in enumerate(new_dataloader):
                    inputs = self._prepare_inputs(inputs)  # 模型输入准备，转成tensor
                    with torch.no_grad():
                        labels = inputs['labels']  # 标签
                        index = inputs['index']    # 索引序号
                        valid_mask = (labels >= 0)  # 构建mask值
                        del inputs['index']   # inputs中删除索引
                        del inputs['labels']  # inputs中删除标签
                        # myinputs是模型的输入
                        myinputs = {
                            "input_ids": inputs["input_ids"],
                            "attention_mask": inputs["attention_mask"],
                        }
                        # out是模型的输出对象
                        output = t_model(**myinputs, output_hidden_states=True)
                        # 有个logists1值（逻辑回归的输出）transformers中model outputs
                        logits1 = output['logits']
                        # embedings 最后一层的embedings*** Extract the embeddings from the last layer of the model
                        embeddings = output['hidden_states'][-1][:, 0, :]
                        # 把embedings保存起来
                        embeddings_all[index] = embeddings.detach().cpu()
                        # logits1作为outputs
                        outputs_all[index] = logits1
                        # labels目标值作为targets
                        targets_all[index] = labels
                        # loss_fct 交叉熵损失模型
                        loss_fct = nn.CrossEntropyLoss(reduction='none')
                        # 计算交叉熵
                        loss = loss_fct(logits1[valid_mask], labels.view(-1)[valid_mask])
                        # 把结果放在loss_all中
                        loss_all[index[valid_mask]] = loss

                high_conf_all = outputs_all.max(dim=-1)[0]  # 最后一维度上的最大值
                pred_idx_all = outputs_all.max(dim=-1)[1]   # 当前索引最后一维度的概率最大值的标签为伪标签
                pred_label_all = pred_idx_all.cpu().tolist()  # 放入 预测标签数组转成列表
                # 把无效的样本用-1打标。filter out the invalid sample with label==-1 (ambiguous annotation by LLM)
                valid_idx_all = targets_all >= 0  # 有效的结果都是>=0
                matched_idx_all = (pred_idx_all == (targets_all)) & valid_idx_all   # matched_idx_all  是预测和目标一致且有效的结果。

                # 健壮的自训练-高斯选择 GMM selection for robust self-training of SLM  bert输出加上了高斯混合模型层。
                # loss的分布调整了一下， (当前值-最小值)/(最大值-最小值)
                # reshape(-1, 1)时，你告诉计算机：“我不关心结果有多少行，只要它有一列就可以了
                loss_all = ((loss_all - loss_all[valid_idx_all].min()) / (
                            loss_all[valid_idx_all].max() - loss_all[valid_idx_all].min())).detach().cpu().reshape(-1,
                                                                                                                   1)
                loss_all_tmp = loss_all[torch.where(valid_idx_all)[0].cpu()]  # 选出有效数据的loss
                gmm = GaussianMixture(n_components=2, max_iter=10, tol=1e-2, reg_covar=5e-4)  # 高斯混合模型
                gmm.fit(loss_all_tmp)  # 模型预测
                prob = gmm.predict_proba(loss_all_tmp)  # 预测概率值
                prob = prob[:, gmm.means_.argmin()]
                chosen_idx_all_gmm = np.where(prob > 0.7)[0]  # 概率值大于0.7的则被选中 （np.where()[0] 表示行的索引；np.where()[1] 则表示列的索引）
                chosen_list[torch.where(valid_idx_all)[0][chosen_idx_all_gmm]] = 1  # chosen_list选择的样本集合标为1（先是有效样本的行，再是概率大于0.7的，然后标上选择=1）

                # 基于类别的演示集构建，将其作为给LLM的反馈，Class-wise demonstration pool construction as feedback to LLM
                chosen_top_indices = []  # 选出top的这批数据
                for j in range(num_labels):  # 从标签集范围中分别一一取出
                    # index_j_matched：j类别中，预测标签和真实标签 匹配上，并且是合法结果的 取出。
                    index_j_matched = torch.where((pred_idx_all == j) & matched_idx_all)[0].cpu()
                    # j类别是最大值的列表
                    max_score_j = high_conf_all[index_j_matched]
                    # 如果空的则跳过
                    if index_j_matched.shape[0] == 0:
                        continue
                    # 最大值降序排序
                    sort_index_j = (-max_score_j).sort()[1].cpu().numpy()
                    # 分区数量
                    partition_j_sel = int((index_j_matched.shape[0]) * rho_sel)
                    if (partition_j_sel) == 0:
                        continue
                    # 再匹配j类别中，按排序取前partition_j_sel的索引
                    index_j_sel = index_j_matched[sort_index_j[:partition_j_sel]]
                    # 选择列表的选中列表中对应索引标上1
                    chosen_list_sel[index_j_sel] = 1
                    # 读取人工更正数据，加载到 manual_label列表
                    with open("../data/manual_label.npy", "rb") as f:
                        manual_label = np.load(f)
                    # 选择集合的选中集中，把manual_label 不为-1（作废），全部加进来。
                    chosen_list_sel[np.where(manual_label != -1)[0]] = 1

                    # 加入手动更新信息Add manual update info
                    with open("../data/manual_label.npy", "rb") as f:
                        manual_label = np.load(f)
                    # 读取人工更正数据（j类别的），加载到 manual_label列表
                    # j为当前j类列的标签，
                    manual_list = np.where(manual_label == j)[0]
                    # manual_list中被选中的样本索引循环取出
                    for manual_idx in manual_list:
                        # 如果不在index_j_sel（j类别选中数据），则将其放入。
                        if manual_idx not in index_j_sel:
                            index_j_sel = torch.cat([index_j_sel, torch.tensor([manual_idx]).cpu()])

                    # 对clean set中数据做k-medoids聚类。For these clean samples [index_j_sel], adopt k-medoids clustering
                    embeddings_j = embeddings_all[index_j_sel]
                    # k-中心聚类计算（取代表性样本） k-medoids for representative samples, 100/2=50 medoids samples
                    # 每个聚簇的样本
                    num_clusters = args.select_demo_num // num_labels
                    # Kmeans的模型创建，并对j类别做聚类- 然后fit计算出聚类结果
                    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(embeddings_j)
                    # 聚类标签列表
                    kmeans_labels = kmeans.labels_
                    # 所有表征性的index数组
                    idx_all_representative = []
                    # 所有表征性的词向量数组
                    embedding_all_representative = []
                    for k in range(num_clusters):
                        # vectors_in_cluster：kmeans标签是k的簇内样本向量聚数组
                        vectors_in_cluster = embeddings_j[kmeans_labels == k]
                        # idx_in_cluster：kmeans标签是k的簇内样本index
                        idx_in_cluster = (index_j_sel)[kmeans_labels == k]
                        # 计算j聚簇中心值
                        centroid = vectors_in_cluster.mean(dim=0)
                        # distances_to_centroid：到中心点的距离，利用torch的范数，在第二个维度计算，默认为p=‘fro’，计算矩阵的Frobenius norm (Frobenius 范数)，就是矩阵各项元素的绝对值平方的总和。
                        distances_to_centroid = torch.norm(vectors_in_cluster - centroid, dim=1)
                        # index_of_representative：（最小的1个）返回输入张量中指定维度的最小值的索引，没有维度参数，则返回所有维度最大
                        index_of_representative = torch.argmin(distances_to_centroid)
                        # embedding_all_representative 表征样本向量加进来
                        embedding_all_representative.append(vectors_in_cluster[index_of_representative])
                        # idx_all_representative 表征样本索引加进来
                        idx_all_representative.append(idx_in_cluster[index_of_representative].reshape(1))

                    # representation and index of samples to be demonstrations
                    embedding_all_representative = torch.cat(
                        #  reshape(1,-1)转化成1行：
                        [emb.reshape(1, -1) for emb in embedding_all_representative])
                    idx_all_representative = torch.cat(idx_all_representative)

                    # 计算相似度 demonstration retrieval for LLMs: similarity between each training example and demonstration sample
                    # 计算所有样本向量和这些表征最强的样本的相似性
                    cos_similarities = cosine_similarity(embeddings_all, embedding_all_representative)
                    # 排序结果：将相似度最高的放前面，降序排序
                    sort_result = torch.sort(torch.from_numpy(cos_similarities), dim=1, descending=True)
                    # 取前shot_num个样本的index
                    top_indices = sort_result[1][:, :(args.shot_num // num_labels)]
                    # similarity-based demonstration retrieval
                    for i in range(top_indices.shape[0]):
                        top_indices[i, :] = idx_all_representative[top_indices[i, :]]
                    #  取出分别放入
                    chosen_top_indices.append(top_indices)

                #  chosen_top_indices：把第二维度的联结
                chosen_top_indices = torch.cat(chosen_top_indices, dim=1)
                # chosen_list_sel中每行的索引拿出来
                chosen_idx_sel = torch.where(chosen_list_sel)[0].cpu()
                # 走的是直推式，并且是epoch==1
                if args.learning_setting == 'transductive' and epoch == 1:
                    import pickle
                    # 保存数据 saving the feedbacks
                    # clean set的索引保存 clean sample index
                    with open("./feedback/right_list_mr.pkl", "wb") as f:
                        pickle.dump(chosen_idx_sel.tolist(), f)
                    # 演示集保存 demonstration retrieval
                    with open("./feedback/demo_index_mr.pkl", "wb") as f:
                        pickle.dump(chosen_top_indices.tolist(), f)
                    # 聚类伪标签保存pseudo-labels for all samples
                    with open("./feedback/pred_label_mr.pkl", "wb") as f:
                        with open("../data/manual_label.npy", "rb") as fm:
                            manual_label = np.load(fm)
                        pred_label_all_new = pred_label_all.copy()  # 预测标签复制
                        if(len(np.where(manual_label != -1)[0])>0): #对空的情况特殊处理
                            #pred_label_all_new[np.int64(np.where(manual_label != -1)[0])] = manual_label[np.where(manual_label != -1)]
                            for idx,manuallabel_infile in enumerate(manual_label):
                                if manuallabel_infile != -1:
                                    pred_label_all_new[idx] = manuallabel_infile                               
                        pickle.dump(pred_label_all_new,f)  #保存预测结果
            if epoch > args.warmup:  # 如果不是预测的epoch，则把数据放入device中
                self.chosen_list = chosen_list.to(args.device)
            else:
                # warm-up phase  预热阶段，用另外的方法
                self.chosen_list = torch.ones_like(chosen_list).to(args.device)

            # end of the sample selection and demonstration construction

            for step, inputs in enumerate(epoch_iterator):
                total_batched_samples += 1
                if rng_to_sync:
                    self._load_rng_state(resume_from_checkpoint)
                    rng_to_sync = False

                # Skip past any already trained steps if resuming training
                if steps_trained_in_current_epoch > 0:
                    steps_trained_in_current_epoch -= 1
                    if steps_trained_progress_bar is not None:
                        steps_trained_progress_bar.update(1)
                    if steps_trained_in_current_epoch == 0:
                        self._load_rng_state(resume_from_checkpoint)
                    continue
                elif steps_trained_progress_bar is not None:
                    steps_trained_progress_bar.close()
                    steps_trained_progress_bar = None

                if step % args.gradient_accumulation_steps == 0:
                    self.control = self.callback_handler.on_step_begin(args, self.state, self.control)

                if (
                        (total_batched_samples % args.gradient_accumulation_steps != 0)
                        and args.local_rank != -1
                        and args._no_sync_in_gradient_accumulation
                ):
                    # Avoid unnecessary DDP synchronization since there will be no backward pass on this example.
                    with model.no_sync():
                        # 3.2 标准的训练和loss计算
                        tr_loss_step = self.training_step(model, inputs)
                else:
                    # 进行训练和loss计算
                    tr_loss_step = self.training_step(model, inputs)

                if (
                        args.logging_nan_inf_filter
                        and not is_torch_tpu_available()
                        and (torch.isnan(tr_loss_step) or torch.isinf(tr_loss_step))
                ):
                    # if loss is nan or inf simply add the average of previous logged losses
                    tr_loss += tr_loss / (1 + self.state.global_step - self._globalstep_last_logged)
                else:
                    tr_loss += tr_loss_step

                self.current_flos += float(self.floating_point_ops(inputs))

                # Optimizer step for deepspeed must be called on every step regardless of the value of gradient_accumulation_steps
                if self.deepspeed:
                    self.deepspeed.step()

                if total_batched_samples % args.gradient_accumulation_steps == 0 or (
                        # last step in epoch but step is always smaller than gradient_accumulation_steps
                        steps_in_epoch <= args.gradient_accumulation_steps
                        and (step + 1) == steps_in_epoch
                ):
                    # Gradient clipping
                    if args.max_grad_norm is not None and args.max_grad_norm > 0 and not self.deepspeed:
                        # deepspeed does its own clipping

                        if self.do_grad_scaling:
                            # Reduce gradients first for XLA
                            if is_torch_tpu_available():
                                gradients = xm._fetch_gradients(self.optimizer)
                                xm.all_reduce("sum", gradients, scale=1.0 / xm.xrt_world_size())
                            # AMP: gradients need unscaling
                            self.scaler.unscale_(self.optimizer)

                        if is_sagemaker_mp_enabled() and args.fp16:
                            self.optimizer.clip_master_grads(args.max_grad_norm)
                        elif hasattr(self.optimizer, "clip_grad_norm"):
                            # Some optimizers (like the sharded optimizer) have a specific way to do gradient clipping
                            self.optimizer.clip_grad_norm(args.max_grad_norm)
                        elif hasattr(model, "clip_grad_norm_"):
                            # Some models (like FullyShardedDDP) have a specific way to do gradient clipping
                            model.clip_grad_norm_(args.max_grad_norm)
                        else:
                            # Revert to normal clipping otherwise, handling Apex or full precision
                            nn.utils.clip_grad_norm_(
                                amp.master_params(self.optimizer) if self.use_apex else model.parameters(),
                                args.max_grad_norm,
                            )

                    # 优化器步骤 Optimizer step
                    optimizer_was_run = True
                    if self.deepspeed:
                        pass  # called outside the loop
                    elif is_torch_tpu_available():
                        if self.do_grad_scaling:
                            self.scaler.step(self.optimizer)
                            self.scaler.update()
                        else:
                            xm.optimizer_step(self.optimizer)
                    elif self.do_grad_scaling:
                        scale_before = self.scaler.get_scale()
                        self.scaler.step(self.optimizer)
                        self.scaler.update()
                        scale_after = self.scaler.get_scale()
                        optimizer_was_run = scale_before <= scale_after
                    else:
                        self.optimizer.step()

                    if optimizer_was_run and not self.deepspeed:
                        self.lr_scheduler.step()

                    model.zero_grad()
                    self.state.global_step += 1
                    self.state.epoch = epoch + (step + 1 + steps_skipped) / steps_in_epoch
                    self.control = self.callback_handler.on_step_end(args, self.state, self.control)

                    self._maybe_log_save_evaluate(tr_loss, model, trial, epoch, ignore_keys_for_eval)
                else:
                    self.control = self.callback_handler.on_substep_end(args, self.state, self.control)

                if self.control.should_epoch_stop or self.control.should_training_stop:
                    break
            if step < 0:
                logger.warning(
                    "There seems to be not a single sample in your epoch_iterator, stopping training at step"
                    f" {self.state.global_step}! This is expected if you're using an IterableDataset and set"
                    f" num_steps ({max_steps}) higher than the number of available samples."
                )
                self.control.should_training_stop = True
            # 结束epoch的切面
            self.control = self.callback_handler.on_epoch_end(args, self.state, self.control)
            # 一些结果统计
            self._maybe_log_save_evaluate(tr_loss, model, trial, epoch, ignore_keys_for_eval)

            if DebugOption.TPU_METRICS_DEBUG in self.args.debug:
                if is_torch_tpu_available():
                    # tpu-comment: Logging debug metrics for PyTorch/XLA (compile, execute times, ops, etc.)
                    xm.master_print(met.metrics_report())
                else:
                    logger.warning(
                        "You enabled PyTorch/XLA debug metrics but you don't have a TPU "
                        "configured. Check your training configuration if this is unexpected."
                    )
            if self.control.should_training_stop:
                break

            #  进度更新，当前进度+1
            progress = {
                'current': epoch + 1 - epochs_trained,
                'total': num_train_epochs - epochs_trained
            }
            # 小模型进度保存
            #with open('../progress/slm_training_progress.json', 'w') as f:
            #    json.dump(progress, f)

        # saving fine-tuned model for computing output information of slm
        # torch.save(model.state_dict(), '../FreeAL-main/self_training_slm/fine_tuned/fine_tuned_model.pt')

        if args.past_index and hasattr(self, "_past"):
            # Clean the state at the end of training
            delattr(self, "_past")

        logger.info("\n\nTraining completed. Do not forget to share your model on huggingface.co/models =)\n\n")
        if args.load_best_model_at_end and self.state.best_model_checkpoint is not None:
            # Wait for everyone to get here so we are sur the model has been saved by process 0.
            if is_torch_tpu_available():
                xm.rendezvous("load_best_model_at_end")
            elif args.local_rank != -1:
                dist.barrier()
            elif is_sagemaker_mp_enabled():
                smp.barrier()

            self._load_best_model()

        # 增加剩下的tr_loss
        # add remaining tr_loss
        self._total_loss_scalar += tr_loss.item()
        # 训练损失值
        train_loss = self._total_loss_scalar / self.state.global_step

        # metrics统计对象
        metrics = speed_metrics("train", start_time, num_samples=num_train_samples, num_steps=self.state.max_steps)
        self.store_flos()
        metrics["total_flos"] = self.state.total_flos
        metrics["train_loss"] = train_loss

        self.is_in_train = False

        self._memory_tracker.stop_and_update_metrics(metrics)

        # 打印出metrics数据
        self.log(metrics)

        run_dir = self._get_output_dir(trial)
        checkpoints_sorted = self._sorted_checkpoints(use_mtime=False, output_dir=run_dir)

        # Delete the last checkpoint when save_total_limit=1 if it's different from the best checkpoint and process allowed to save.
        if self.args.should_save and self.state.best_model_checkpoint is not None and self.args.save_total_limit == 1:
            for checkpoint in checkpoints_sorted:
                if checkpoint != self.state.best_model_checkpoint:
                    logger.info(f"Deleting older checkpoint [{checkpoint}] due to args.save_total_limit")
                    shutil.rmtree(checkpoint)

        # 训练结束控制点
        self.control = self.callback_handler.on_train_end(args, self.state, self.control)
        # 返回结果
        return TrainOutput(self.state.global_step, train_loss, metrics)

    # 3.2.2计算损失
    def compute_loss(self, model, inputs, return_outputs=False):
        # for name, layer in model.named_modules():
        #     print(name)
        w = linear_rampup(self.state.epoch, 10)  # 计算损失前10步学习率线性增加
        is_in_train = ("input_ids_bt" in inputs.keys())

        labels = inputs.get("labels") # 获取标签
        if is_in_train:  # 带回译的
            valid_mask = (labels >= 0)
            batch_index = inputs['index']
            batch_mask = self.chosen_list[batch_index]
            batch_mask = batch_mask.bool() & valid_mask
            batch_mask_un = ~(self.chosen_list[batch_index].bool()) & valid_mask
        else:  # 正常计算
            batch_mask = torch.ones_like(labels)  # mask值
            batch_mask_un = torch.zeros_like(labels) # 反向mask
        index_x = torch.where(batch_mask)[0] # index_x mask的
        index_u = torch.where(batch_mask_un)[0] # index_x unmask的

        # 输入数据
        myinputs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
        }

        # output = model(**myinputs,output_hidden_states=True)
        # logits = output['logits']
        # # *** Extract the embeddings from the last layer of the model
        # embeddings = output['hidden_states'][-1][:,0,:]

        # 模型计算embedings
        embeddings = model.roberta(**myinputs)[0]
        # 模型执行全连接分类层，结果放到logits
        logits = model.classifier(embeddings)

        # 交叉熵损失
        loss_fct = nn.CrossEntropyLoss(reduction='none')
        # KL散度损失
        loss_fct_un = nn.KLDivLoss(reduction='sum')

        # loss_l值：在筛选出来的clean set的交叉熵损失，并计算均值。cross-entropy loss on filtered clean subset
        loss_l = loss_fct(logits[index_x], labels.view(-1)[index_x]).mean()

        # 向量级别的混合策略模型 embedding-level mix-up stragety on clean subset
        valid_embeddings = embeddings[index_x]
        # 梯度归零
        with torch.no_grad():
            # 标签转成one_hot编码
            targets_l = F.one_hot(labels[index_x].detach(), num_classes=self.num_labels)
            # 所有的targets编号
            all_targets = targets_l.detach()
        # 在 PyTorch 中,torch.randperm(n) 函数用于生成一个从 0 到 n-1 的随机排列的整数序列
        rand_idx = torch.randperm(valid_embeddings.size(0))
        # 狄利克雷分布的两类场景-beta分布，https://zhuanlan.zhihu.com/p/24555092
        l = np.random.beta(4, 4)
        l = max(l, 1 - l)  # 取两边概率大这侧为l
        #  混合嵌入：自己*（l）+任意非自己的（1-l）
        mixed_embeddings = l * valid_embeddings + (1 - l) * valid_embeddings[rand_idx]
        #  混合target：目标targets*（l）+任意非自己的tagets（1-l）
        mixed_targets = l * all_targets + (1 - l) * all_targets[rand_idx]
        #  获取一个混合逻辑回归的值
        mixed_logits = model.classifier(mixed_embeddings)
        # 混合的softmax除开一个loss均值（感觉像带了噪音、扰动）
        loss_mix = -torch.mean(torch.sum(F.log_softmax(mixed_logits, dim=-1) * mixed_targets, dim=-1))
        # 合出了一个综合loss（这样可能是说更加健壮了）
        final_loss = (loss_l) + w * loss_mix

        # 如果带回译的数据增广，则使用一致性归一。in training: utilize consistency regularization on all data
        if is_in_train:
            myinputs_bt = {
                "input_ids": inputs["input_ids_bt"],
                "attention_mask": inputs["attention_mask_bt"],
            }
            embeddings_bt = model.roberta(**myinputs_bt)[0]
            logits_bt = model.classifier(embeddings_bt)
            loss_cr = loss_fct(logits_bt[index_x], labels.view(-1)[index_x]).mean()
            loss_cr_un = 0.5 * loss_fct_un(F.log_softmax(logits[index_u] / self.temp_u, dim=-1),
                                           F.softmax(logits_bt[index_u].detach().clone(), dim=-1)) + 0.5 * loss_fct_un(
                F.log_softmax(logits_bt[index_u] / self.temp_u, dim=-1),
                F.softmax(logits[index_u].detach().clone(), dim=-1))
            final_loss = final_loss + w * (loss_cr + loss_cr_un)

        # 返回最终的loss值或outputs输出
        return (final_loss, {'outputs': logits}) if return_outputs else final_loss

    # 3.2 标准的训练和loss计算（训练执行步骤）
    def training_step(self, model: nn.Module, inputs: Dict[str, Union[torch.Tensor, Any]]) -> torch.Tensor:
        # 3.2.1 网络模型torch训练
        model.train()
        inputs = self._prepare_inputs(inputs)
        # 1.2计算损失
        with self.compute_loss_context_manager():
            # 3.2.2计算损失
            loss = self.compute_loss(model, inputs)

        if self.args.gradient_accumulation_steps > 1 and not self.deepspeed:
            # deepspeed handles loss scaling by gradient_accumulation_steps in its `backward`
            loss = loss / self.args.gradient_accumulation_steps

        # 3.2.3反向传播
        if self.do_grad_scaling:
            self.scaler.scale(loss).backward()
        elif self.use_apex:
            with amp.scale_loss(loss, self.optimizer) as scaled_loss:
                scaled_loss.backward()
        elif self.deepspeed:
            # loss gets scaled under gradient_accumulation_steps in deepspeed
            loss = self.deepspeed.backward(loss)
        else:
            loss.backward()  # loss反向传播
        return loss.detach()