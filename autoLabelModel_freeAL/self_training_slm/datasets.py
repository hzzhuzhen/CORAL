import os
import torch
import tqdm
import logging
import csv
from torch.utils.data.dataset import Dataset
from transformers import PreTrainedTokenizer
from typing import List, Optional,Dict
from dataclasses import dataclass
from filelock import FileLock
from transformers import pipeline

logger = logging.getLogger(__name__)

# 数据处理,装入数据结构
class MyDataCollator:
    def __init__(self):
        pass
    
    def __call__(self, examples: List[Dict[str, torch.Tensor]]) -> Dict[str, torch.Tensor]:
        if isinstance(examples[0],dict):
            #with data-augmentation through backtranslation
            inputs = [example["inputs"] for example in examples]  # 输入数据数据
            inputs_bt = [example["inputs_bt"] for example in examples]  # 输入数据回译
            index = [ip.index for ip in inputs]  # 输入数据的编号
            input_ids = [ip.input_ids for ip in inputs]  # 数据向量编码
            attention_mask = [ip.attention_mask for ip in inputs]  # 数据的注意力mask
            label = [ip.label for ip in inputs]  # 数据的标签
            input_ids_bt = [ip_bt.input_ids for ip_bt in inputs_bt]  # 输入数据回译的向量编码
            attention_mask_bt = [ip_bt.attention_mask for ip_bt in inputs_bt]  # 输入数据回译的注意力mask
            batch = {  # 全部转成tensor
                'index': torch.tensor(index),
                'input_ids': torch.tensor(input_ids),
                'attention_mask': torch.tensor(attention_mask),
                'labels': torch.tensor(label),
                'input_ids_bt': torch.tensor(input_ids_bt),
                'attention_mask_bt': torch.tensor(attention_mask_bt),
            }
            
        else:
            #数据不做增广（即回译）without data augmentation
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

# 数据集输入数据的样例
# 内容，内容回译，标签
@dataclass
class DatasetInputExample:
    
    contents: str
    contents_bt: str
    label: Optional[int]
        
# 数据集输入特征
# 索引、词向量、注意力mask、token类型（分句编号啥的）、标签
@dataclass
class DatasetInputFeature:
    
    index: int
    input_ids: List[int]
    attention_mask: Optional[List[List[int]]]
    token_type_ids: Optional[List[List[int]]]
    label: Optional[int]
            
# 分类数据数据集处理器
class ClassificationDataset(Dataset):

    features: List[DatasetInputFeature]  # 数据集转成特征结构

    def __init__(
        self,
        data_dir: str,  # 数据集目录
        tokenizer: PreTrainedTokenizer,  # 训练的分词器
        task: str,  # 任务名称
        max_seq_length: Optional[int] = None,  # 最大句子序列长度
        overwrite_cache=False,
        mode: str = "train",  # 模式标记
    ):

        processor = ClassificationProcessor()  # 创建数据处理器对象
        self.mode = mode  # 模型获取
        cached_features_file = os.path.join(
            data_dir,
            "cached_{}_{}_{}_{}".format(mode, tokenizer.__class__.__name__, str(max_seq_length), task,),
        )  # 缓存特征化的数据文件

        # 第一次数据处理会处理数据，后面直接使用缓存
        # Make sure only the first process in distributed training processes the dataset,
        # and the others will use the cache.
        lock_path = cached_features_file + ".lock"
        with FileLock(lock_path):  # 如果有缓存数据则从缓存数据中load进来
            if os.path.exists(cached_features_file) and not overwrite_cache:
                logger.info(f"Loading features from cached file {cached_features_file}")
                self.features = torch.load(cached_features_file)
            else:  # 没有缓存，则从数据源读取
                logger.info(f"Creating features from dataset file at {data_dir}")
                data_dir = os.path.join(data_dir,task)
                # 跑的是不同模式，则从不同的数据来源读取。
                if mode == "dev":
                    examples = processor.get_dev_examples(data_dir)
                elif mode == "test":
                    examples = processor.get_test_examples(data_dir)
                elif mode == "train_chat":
                    examples = processor.get_train_chat_examples(data_dir)
                else:
                    examples = processor.get_train_examples(data_dir)

                logger.info("Training examples: {}".format(len(examples)))
                self.features = convert_examples_to_features(examples, max_seq_length, tokenizer,mode)
                logger.info("Saving features into cached file {}".format(cached_features_file))
                torch.save(self.features, cached_features_file)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, i):
        if self.mode == "train_chat":
            return self.features[i]
        else:
            return self.features[i]
    
class DataProcessor:
    """Base class for data converters for multiple choice data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_train_chat_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_test_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the test set."""
        raise NotImplementedError()
    
# 分类器处理器
class ClassificationProcessor(DataProcessor):
    # 获取训练用例的样本
    def get_train_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {} train".format(data_dir))
        train = self._read_csv(data_dir, "train")

        return self._create_examples(train,"train")
    # 获取扩增后的训练数据集
    def get_train_chat_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {} train chat".format(data_dir))
        train_chat = self._read_csv(data_dir, "train_chat_bt")
        
        return self._create_examples(train_chat,"train_chat")

    # 获取dev数据集
    def get_dev_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {} dev".format(data_dir))
        dev = self._read_csv(data_dir, "dev")
        
        return self._create_examples(dev,"dev")

    # 获取测试数据集
    def get_test_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {} test".format(data_dir))
        test = self._read_csv(data_dir, "test")
        
        return self._create_examples(test,"test")

    # 读CSV数据
    def _read_csv(self, input_dir, set_type):
        corpus = []
        with open("{}/{}.csv".format(input_dir, set_type), 'r', encoding='utf-8') as f:
            data = csv.reader(f)  # 读数据
            if set_type == "train_chat_bt":  # 机器人回译数据
                for line in data:
                    if len(line) == 1:  # 只有一列，直接读入
                        corpus.append([line[0]])
                    elif len(line) == 2:  # 有两行，先放第二列，再放第一列
                        corpus.append([line[1], int(line[0])])
                    else:  # 如果有三列，第二列先，第一列是次列，最后列还是放在最后
                        corpus.append([line[1], int(line[0]), line[2]])
            else:  # 其他所有数据类型
                for line in data:
                    if len(line) == 1:
                        corpus.append([line[0]])
                    else:  # 第二列放前，第一列放后
                        corpus.append([line[1], int(line[0])])

        return corpus

    # 创建样例数据集结构对象
    def _create_examples(self, corpus, mode):
        """Creates examples for the training and dev sets."""
        examples = []
        for data in tqdm.tqdm(corpus, desc="creating examples for "+mode):
    
            if mode == "train_chat":  # 如果train_chat 才会有contents_bt的数据
                contents_bt = data[2]#pipe_bt(pipe(data[0])[0]["translation_text"])[0]["translation_text"]
            else:
                contents_bt = None  # 其他都没有这个数据内容
            examples.append(
                DatasetInputExample(
                    contents=data[0],  # 第一个数据是content的
                    contents_bt = contents_bt,
                    label=data[1] if len(data) == 2 or len(data) == 3 else None  # 第2个位置的是label
                )
            )
        return examples

# 将样例内容转成features特征向量对象
def convert_examples_to_features(
    # 样例数据： 文本形式输入数据集集合、最大长度、分词器、模型
    examples: List[DatasetInputExample], max_length: int, tokenizer: PreTrainedTokenizer, mode):
    """
    Loads a data file into a list of `DatasetInputExample`
    """

    features = []
    # for循环取出数据处理
    for (ex_index, example) in tqdm.tqdm(enumerate(examples), desc="convert examples to features"):
        if ex_index % 10000 == 0:
            logger.info("\nWriting example {} of {}".format(ex_index, len(examples)))

        # 输入分词器，输出词向量
        inputs = tokenizer(
            example.contents,
            max_length=max_length,
            add_special_tokens=True,
            padding="max_length",
            truncation=True
        )
        
        # a.train_chat特殊类型数据，放入inputs和inputs_bt两类数据到DatasetInputFeature
        if mode == "train_chat":
            inputs_bt = tokenizer(
                example.contents_bt,
                max_length=max_length,
                add_special_tokens=True,
                padding="max_length",
                truncation=True
            )
            features.append({
                "inputs":
                DatasetInputFeature(
                    index = ex_index,
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask if "attention_mask" in inputs else None,
                    token_type_ids=None,
                    label=example.label
                ),
                "inputs_bt":
                DatasetInputFeature(
                    index = ex_index,
                    input_ids=inputs_bt.input_ids,
                    attention_mask=inputs_bt.attention_mask if "attention_mask" in inputs_bt else None,
                    token_type_ids=None,
                    label=example.label
                ),
                }
            )
        else:  # b.普通类型数据，放inputs到DatasetInputFeature
            features.append(
                DatasetInputFeature(
                    index = ex_index,
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask if "attention_mask" in inputs else None,
                    token_type_ids=None,
                    label=example.label
                )
            )
            
    # 特征数据输出
    for f in features[:2]:
        logger.info("*** Example ***")
        logger.info("feature: {}".format(f))

    return features
