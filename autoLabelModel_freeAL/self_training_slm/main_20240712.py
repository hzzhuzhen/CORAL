from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    Trainer,
    HfArgumentParser,
    set_seed,
    AutoModel
)
from transformers.trainer import *
from modeling import MODEL, AutoTokenizer
from datasets import ClassificationDataset, MyDataCollator
from arguments import ModelArguments, DataTrainingArguments, TrainingArguments
from utils.utils import set_logger, path_checker, metrics_fn
from runner import Runner
import torch
from torch import nn
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union
from torch.nn import CrossEntropyLoss, KLDivLoss, NLLLoss, BCEWithLogitsLoss
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
from mytrainer import MyTrainer
from typing import List, Dict

from torch.utils.data import DataLoader, Dataset

from torch.nn import CrossEntropyLoss, KLDivLoss, NLLLoss, BCEWithLogitsLoss
from sklearn.metrics import confusion_matrix ,recall_score,roc_auc_score, accuracy_score, f1_score
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import pandas as pd

from tqdm import tqdm
# my_collate_fn 对数据做前置处理和确认
def my_collate_fn(examples):
    if isinstance(examples[0],dict):
        #with data-augmentation through backtranslation
        # 通过数据回译的数据扩增
        inputs = [example["inputs"] for example in examples]
        inputs_bt = [example["inputs_bt"] for example in examples]
        index = [ip.index for ip in inputs]
        input_ids = [ip.input_ids for ip in inputs]
        attention_mask = [ip.attention_mask for ip in inputs]
        label = [ip.label for ip in inputs]
        input_ids_bt = [ip_bt.input_ids for ip_bt in inputs_bt]
        attention_mask_bt = [ip_bt.attention_mask for ip_bt in inputs_bt]
        batch = {
            'index': torch.tensor(index),
            'input_ids': torch.tensor(input_ids),
            'attention_mask': torch.tensor(attention_mask),
            'labels': torch.tensor(label),
            'input_ids_bt': torch.tensor(input_ids_bt),
            'attention_mask_bt': torch.tensor(attention_mask_bt),
        }
        
    else:
        #without data augmentation
        # 没有数据扩增的分支
        index = [example.index for example in examples]
        input_ids = [example.input_ids for example in examples]
        attention_mask = [example.attention_mask for example in examples]
        label = [example.label for example in examples]
        batch = {
            'index': torch.tensor(index),
            'input_ids': torch.tensor(input_ids),
            'attention_mask': torch.tensor(attention_mask),
            'labels': torch.tensor(label),
        }
    return batch
    
# 小模型结果输出展示
def output_info(args, model, fine_tuned, dataset, refinery):
    if os.path.exists(fine_tuned):
        model.load_state_dict(torch.load(fine_tuned))  # 获取微调后的model
    model.eval().to(args.device)  # 简而言之，就是评估模式。而非训练模式。在评估模式下，batchNorm层，dropout层等用于优化训练而添加的网络层会被关闭，从而使得评估时不会发生偏移。
    dataloader = DataLoader(dataset, batch_size=256, shuffle=False, collate_fn=my_collate_fn)  # 加载数据
    length = len(dataset)
    logits_list = torch.zeros((length,args.num_labels)).cuda()  # 输出 logits_list.shape() = 数据集长度*标签数量
    embeddings_list = torch.zeros((length,args.embedding_dim))  # 输出 embeddings_list = 数据集长度 * 嵌入维度dim
    loss_list = torch.zeros(length).cuda()  # 输出 loss_list = 每个样本的损失值的list
    targets_all = torch.zeros((length), dtype=torch.long).cuda()  # 目标值的list
    demo_list = torch.zeros((length)).cuda()  # 演示集合数据的list
    for step, inputs in enumerate(tqdm(dataloader)):  # tqdm python的进度条
        with torch.no_grad():
            intputs = inputs
            labels = inputs['labels'].to(args.device)  # 标签栏数据，返回1维list
            index = inputs['index'].to(args.device)    # 索引值，返回1维list（因为这里有可能是乱序的给过来的）
            targets_all[index] = labels  # 标签打标的的数据按索引顺序放入targets_all
            valid_mask = (labels >= 0)  # 标签值>=0认为是有效标签，-1是无效标签
            del inputs['index']  # 删除index列
            del inputs['labels']  # 删除标签列
            myinputs = {  # 构建新的输入数据myinputs牟其中label已经被删掉了
                "input_ids": inputs["input_ids"].to(args.device),
                "attention_mask": inputs["attention_mask"].to(args.device),
            }
            output = model(**myinputs,output_hidden_states=True)  #  运行模型给出输出
            logits = output['logits']  # output的logits值就是类别概率
            # *** Extract the embeddings from the last layer of the model
            embeddings = output['hidden_states'][-1][:,0,:]   # 模型最后一层的隐层抽取来，都是取了CLS这位的数据。

            logits_list[index] = logits  # 结果放在logits_list对应index位置上
            embeddings_list[index] = embeddings.detach().cpu()  # embeding输出也放在对应index位置上。
            # print(logits, embeddings)

            
            loss_fct = nn.CrossEntropyLoss(reduction='none')
            loss = loss_fct(logits[valid_mask], labels.view(-1)[valid_mask])  # 对比结果计算交叉熵
            loss_list[index[valid_mask]] = loss  # 放入有效的loss+list中
    
    valid_idx_all = (targets_all >= 0)  # targets_all list的真实标签数据 > 0则保留
    loss_list = ((loss_list-loss_list[valid_idx_all].min())/(loss_list[valid_idx_all].max()-loss_list[valid_idx_all].min())).detach().cpu().reshape(-1,1)  #loss标准化 当前值减去最小值，
    loss_list_tmp = loss_list[torch.where(valid_idx_all)[0].cpu()]  # 有效的loss的list单独取出。
    gmm = GaussianMixture(n_components=2,max_iter=10,tol=1e-2,reg_covar=5e-4)
    gmm.fit(loss_list_tmp) # 双峰GMM去拟合
    prob = gmm.predict_proba(loss_list_tmp)  # gmm输出预测概率prob
    prob = prob[:,gmm.means_.argmin()]  # prob中基于设定的阈值取出满足条件的clean set。
    prob_list = torch.zeros(length, dtype=torch.double).cpu()  # prob_list 构造一个 length长度的概率列表
    prob_list[torch.where(valid_idx_all)[0].cpu()] = torch.from_numpy(prob)  #数据转化后放入torch的list中
    
    rank = (torch.argsort(prob_list,descending=True) + 1) # 对数据做降序排序
    
    # print(logits_list.shape, embeddings_list.shape)
    
    coordinates_list = embeddings_decomposition(embeddings_list.detach().cpu().numpy())  # 降为到二维空间，输出到坐标上。
    # print(coordinates_list.shape)
    
    confidence_list, labels_slm = torch.max(nn.functional.softmax(logits_list, dim=1), dim=1)  # 对逻辑概率列表，通过softmax输出lablels结果。
    confidence_list = confidence_list.detach().cpu()  # 置信度转成CPU
    # print(confidence_list.shape)
    # print(labels_slm.shape)

    matched_idx_all = (labels_slm==(targets_all))&valid_idx_all  # 计算标签匹配的数据
    high_conf_all = logits_list.max(dim=-1)[0]  # 倒数第一维度的数据取最大，返回到high_conf_all
    chosen_top_indices = []
    rho_sel = 0.2
    chosen_list_sel = torch.zeros((length)).cuda()  # 构建选择列表

    for j in range(args.num_labels):  # 每个标签分别循环过来
        index_j_matched = torch.where((labels_slm==j)&matched_idx_all)[0].cpu()  # j标签且小模型输出和真实匹配的index。
        max_score_j = high_conf_all[index_j_matched]  # 同时存在于高置信列表+max_score_j的取出
        if index_j_matched.shape[0]==0:
            continue
        sort_index_j = (-max_score_j).sort()[1].cpu().numpy()  # 排序
        partition_j_sel = int((index_j_matched.shape[0])*rho_sel)  # 行数*rho_sel
        if (partition_j_sel) == 0:
            continue
        index_j_sel = index_j_matched[sort_index_j[:partition_j_sel]]  # 取一定比例的行
        chosen_list_sel[index_j_sel] = 1  # 选中的这些索引标记为1

        with open("../data/labels_manual.npy", "rb") as f:
            manual_label = np.load(f)  # 读取手工标记的数据

        chosen_list_sel[np.where(manual_label != -1)[0]] = 1  # 数据为-1为未标注，这些数据去掉，先把index拿出来放入chosen_list_sel

        # Add manual update info
        with open("../data/labels_manual.npy", "rb") as f:
            manual_label = np.load(f)

        manual_list = np.where(manual_label == j)[0]  # 把index放入到手动更正manual_list中

        for manual_idx in manual_list:
            if manual_idx not in index_j_sel:
                index_j_sel = torch.cat([index_j_sel, torch.tensor([manual_idx])])  # 手动列表不存在则一个个更新进去。

        # For these clean samples [index_j_sel], adopt k-medoids clustering
        embeddings_j = embeddings_list[index_j_sel] # 把选中集合的embeddings_j取出
        # k-medoids for representative samples, 100/2=50 medoids samples
        num_clusters = args.select_demo_num//args.num_labels  #  表征性样本（簇数中样本数量）
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(embeddings_j)
        kmeans_labels = kmeans.labels_    # kmeans_labels的聚类伪标签。
        idx_all_representative = []  # 表征性样本的idx数组
        embedding_all_representative = []  # 表征性样本的embedding数组
        for k in range(num_clusters):  # [1,2,3...num_clusters] 聚类簇的数量
            vectors_in_cluster = embeddings_j[kmeans_labels==k]  # 取出第k个伪标签对应样本向量（应该有多个）
            idx_in_cluster = (index_j_sel)[kmeans_labels==k]  # 取出对应样本索引
            centroid = vectors_in_cluster.mean(dim=0)  # 对这些样本取中值 centroid
            distances_to_centroid = torch.norm(vectors_in_cluster - centroid, dim=1)   #计算每个样本到中心点的距离
            index_of_representative = torch.argmin(distances_to_centroid)  # 取出这里面距离最小的样本的index
            embedding_all_representative.append(vectors_in_cluster[index_of_representative])  # 把这个index对应的向量装入到embedding_all_representative（表征样本集）
            idx_all_representative.append(idx_in_cluster[index_of_representative].reshape(1))  # 把这个index装入idx_all_representative（表征样本集）

        #representation and index of samples to be demonstrations 这里两个集合对应到演示样本集
        embedding_all_representative = torch.cat([emb.reshape(1,-1) for emb in embedding_all_representative])
        idx_all_representative = torch.cat(idx_all_representative)

        #demonstration retrieval for LLMs: similarity between each training example and demonstration sample
        cos_similarities = cosine_similarity(embeddings_list, embedding_all_representative)  # 计算样本集合和所有样本的相似度
        sort_result = torch.sort(torch.from_numpy(cos_similarities), dim=1, descending=True)  # 降序排列这个相似度到sort_result
        top_indices = sort_result[1][:, :(args.shot_num//args.num_labels)]  # 数据给每个标签找top几个样本作为top_indices
        #similarity-based demonstration retrieval  基于样四度的样本集检索
        for i in range(top_indices.shape[0]):
            top_indices[i,:] = idx_all_representative[top_indices[i,:]]
        chosen_top_indices.append(top_indices)  #  把这个数据放入到 chosen_top_indices

    labels_slm = labels_slm.detach().cpu()

    chosen_top_indices = torch.cat(chosen_top_indices,dim=1)
    for demo_idx in chosen_top_indices:
        demo_list[demo_idx] = 1  #  生成demo选中的一个列表
    if refinery:
        with open('../data/confidence_list_refinery.npy', 'wb') as f:
            print(confidence_list.shape)
            np.save(f, confidence_list.tolist())  # 置信度列表保存
            df = pd.DataFrame({'data': confidence_list.tolist()})
            df.to_csv('../data/confidence_list_refinery.csv', index=True, header=False)   

        with open('../data/coordinates_list_refinery.npy', 'wb') as f:
            print(coordinates_list.shape)
            np.save(f, coordinates_list)  # 坐标列表保存
            df = pd.DataFrame({'data': coordinates_list.tolist()})
            df.to_csv('../data/coordinates_list_refinery.csv', index=True, header=False)    

        with open('../data/rank_list_refinery.npy', 'wb') as f:
            print(rank.shape)
            np.save(f, rank.tolist())  # 排序列表保存
            df = pd.DataFrame({'data': rank.tolist()})
            df.to_csv('../data/rank_list_refinery.csv', index=True, header=False) 

        with open('../data/labels_slm_refinery.npy', 'wb') as f:
            print(labels_slm.shape)
            np.save(f, labels_slm.tolist())  # 小模型生成标签
            df = pd.DataFrame({'data': labels_slm.tolist()})
            df.to_csv('../data/labels_slm_refinery.csv', index=True, header=False) 

        with open('../data/demo_list_refinery.npy', 'wb') as f:
            print(demo_list.shape)
            np.save(f, demo_list.tolist())  # 演示集数据
            df = pd.DataFrame({'data': demo_list.tolist()})
            df.to_csv('../data/demo_list_refinery.csv', index=True, header=False) 

    else:
        with open('../data/confidence_list.npy', 'wb') as f:
            print(confidence_list.shape)
            np.save(f, confidence_list.tolist())  # 普通的置信度列表
            df = pd.DataFrame({'data': confidence_list.tolist()})
            df.to_csv('../data/confidence_list.csv', index=True, header=False)    

        with open('../data/coordinates_list.npy', 'wb') as f:
            print(coordinates_list.shape)
            np.save(f, coordinates_list)  # 普通坐标列表
            df = pd.DataFrame({'data': coordinates_list.tolist()})
            df.to_csv('../data/coordinates_list.csv', index=True, header=False)    

        with open('../data/rank_list.npy', 'wb') as f:
            print(rank.shape)
            np.save(f, rank.tolist())  #排序列表
            df = pd.DataFrame({'data': demo_list.tolist()})
            df.to_csv('../data/rank_list.csv', index=True, header=False) 

        with open('../data/labels_slm.npy', 'wb') as f:
            print(labels_slm.shape)
            np.save(f, labels_slm.tolist())  #普通小模型打标列表
            df = pd.DataFrame({'data': labels_slm.tolist()})
            df.to_csv('../data/labels_slm.csv', index=True, header=False)        

        with open('../data/demo_list.npy', 'wb') as f:
            print(demo_list.shape)
            np.save(f, demo_list.tolist())  #普通大模型打标列表
            df = pd.DataFrame({'data': demo_list.tolist()})
            df.to_csv('../data/demo_list.csv', index=True, header=False)

    return {"confidence": confidence_list.tolist(), "coordintates": coordinates_list, "rank": rank.tolist(), "labels": labels_slm.tolist()}

# 词向量分解（PCA主成分分析）
def embeddings_decomposition(representation_list):
    # *** Map the embeddings to the new space
    # *** You can use PCA, t-SNE, UMAP, or any other dimensionality reduction technique
    # *** Here, we use PCA
    pca = PCA(n_components=2)
    pca.fit(representation_list)
    reduced_data = pca.fit_transform(representation_list)
    return reduced_data

### 小模型运行入口
def main():
    # Get arguments 获取参数
    parser = HfArgumentParser(
        (ModelArguments, DataTrainingArguments, TrainingArguments)
    )
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()
    training_args.num_labels = data_args.num_labels

    # Path check and set logger
    path_checker(training_args)
    set_logger(training_args)
    # 是否为refinery阶段
    refinery =training_args.refinery

    # Get model name 读取种子
    model_name = (
        model_args.model_name_or_path
        if model_args.model_name_or_path is not None
        else (
            MODEL[model_args.model.lower()]
            if model_args.model.lower() in MODEL
            else model_args.model
        )
    )

    # Set seed  设置种子
    set_seed(training_args.seed)

    # Set model
    # config = AutoConfig.from_pretrained(
    #     model_args.config_name if model_args.config_name else model_name,
    #     cache_dir=model_args.cache_dir,
    #     num_labels=data_args.num_labels,
    # )
    # tokenizer = AutoTokenizer.from_pretrained(
    #     model_args.tokenizer_name if model_args.tokenizer_name else model_name,
    #     cache_dir=model_args.cache_dir,
    # )

    # model = AutoModelForSequenceClassification.from_pretrained(
    #     model_name, config=config, cache_dir=model_args.cache_dir
    # )
    # 模型加载
    config = AutoConfig.from_pretrained("./models/roberta-base", local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained("./models/roberta-base", local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained("./models/roberta-base", config=config, local_files_only=True)
    # 扩增的训练数据集（带回译）
    train_aug = (
        ClassificationDataset(
            data_args.data_dir,
            tokenizer,
            data_args.task_name,
            data_args.max_seq_length,
            data_args.overwrite_cache,
            mode="train_chat",
        )
        if training_args.do_train
        else None
    )
    # 构建训练数据集
    train = (
        ClassificationDataset(
            data_args.data_dir,
            tokenizer,
            data_args.task_name,
            data_args.max_seq_length,
            data_args.overwrite_cache,
            mode="train",
        )
        if training_args.do_train
        else None
    )
    # 构建开发数据集
    dev = (
        ClassificationDataset(
            data_args.data_dir,
            tokenizer,
            data_args.task_name,
            data_args.max_seq_length,
            data_args.overwrite_cache,
            mode="dev",
        )
        if training_args.do_eval
        else None
    )
    # 构建测试数据集
    test = (
        ClassificationDataset(
            data_args.data_dir,
            tokenizer,
            data_args.task_name,
            data_args.max_seq_length,
            data_args.overwrite_cache,
            mode="test",
        )
        if training_args.do_predict
        else None
    )
    # 两种模式：1transductive直推模式（用训练集验证），2.inductive归纳模式（用测试集验证）
    if data_args.learning_setting == "transductive":
        # transductive setting
        eval_dataset = train
    else:
        # inductive setting
        eval_dataset = test
    training_args.learning_setting = data_args.learning_setting

    # 构建训练器
    trainer = MyTrainer(
        model=model,
        args=training_args,
        train_dataset=train_aug,
        eval_dataset=eval_dataset,
        compute_metrics=metrics_fn,
        data_collator=MyDataCollator(),
    )
    #  执行器
    # Set runner
    runner = Runner(
        model_name=model_name,
        trainer=trainer,
        tokenizer=tokenizer,
        training_args=training_args,
        test=test,
        eval=dev,
    )
    # 开始运行代码
    # Start
    runner()
    # 小模型过程信息输出
    #SLMOutputInfo = output_info(args=training_args, model=model, fine_tuned="/data/home/Lin_Long/VLDB_Demo/FreeAL-main/self_training_slm/fine_tuned/1st_round_slm.pt", dataset=train)
    # runner()

    #refinery = False
    if refinery:
        fine_tuned = 'fine_tuned/2nd_round_slm.pt'
    else:
        fine_tuned = 'fine_tuned/1st_round_slm.pt'

    # 小模型过程信息输出
    SLMOutputInfo = output_info(args=training_args, model=model, fine_tuned=fine_tuned, dataset=train, refinery=refinery)
    print(SLMOutputInfo)


if __name__ == "__main__":
    main()
