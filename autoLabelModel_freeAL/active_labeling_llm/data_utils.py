import os
import logging
import csv
from typing import List, Optional, Dict
from dataclasses import dataclass
import tqdm
import pandas as pd


logger = logging.getLogger(__name__)

@dataclass
class DatasetInputExample:
    
    contents: str
    contents_bt: str
    label: Optional[int]

class DataProcessor:
    """Base class for data converters for multiple choice data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_train_bt_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_test_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the test set."""
        raise NotImplementedError()
    
    
class ClassificationProcessor(DataProcessor):
    
    def get_train_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {} train".format(data_dir))
        train = self._read_csv(data_dir)

        return self._create_examples(train)
    
    def get_train_bt_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {} train bt ".format(data_dir))
        train_chat = self._read_bt_csv(data_dir)
        
        return self._create_bt_examples(train_chat)

    
    # def get_dev_examples(self, data_dir):
    #     """See base class."""
    #     logger.info("LOOKING AT {} dev".format(data_dir))
    #     dev = self._read_csv(data_dir, "dev")
        
    #     return self._create_examples(dev,"dev")

    
    # def get_test_examples(self, data_dir):
    #     """See base class."""
    #     logger.info("LOOKING AT {} test".format(data_dir))
    #     test = self._read_csv(data_dir, "test")
        
    #     return self._create_examples(test,"test")

    
    def _read_csv(self, data_dir):
        corpus = []
        with open(data_dir, 'r', encoding='utf-8') as f:
            data = csv.reader(f)
            for line in data:
                if len(line) == 1:
                    corpus.append([line[0]])
                else:
                    corpus.append([line[1], int(line[0])])
        return corpus
    def _read_bt_csv(self, data_dir):
        corpus = []
        with open(data_dir, 'r', encoding='utf-8') as f:
            data = csv.reader(f)
            for line in data:
                if len(line) == 1:
                    corpus.append([line[0]])
                elif len(line) ==3:
                    corpus.append([line[1],line[2], int(line[0])])
                else:
                    corpus.append([line[1], int(line[0])])
        return corpus
    
    def _create_examples(self, corpus):
        """Creates examples for the training and dev sets."""
        examples = []
        for data in tqdm.tqdm(corpus, desc="creating examples"):
            contents_bt = None
            examples.append(
                DatasetInputExample(
                    contents=data[0],
                    contents_bt = contents_bt,
                    label=data[1] if len(data) == 2 or len(data) == 3 else None
                )
            )
        return examples
    def _create_bt_examples(self, corpus):
        """Creates examples for the training bt sets."""
        examples = []
        for data in tqdm.tqdm(corpus, desc="creating examples"):
            contents_bt = None
            examples.append(
                DatasetInputExample(
                    contents=data[0],
                    contents_bt = data[1],
                    label=data[2]
                )
            )
        return examples    
    
def get_user_data(data_dir="data/train.csv"):
    processor = ClassificationProcessor()
    data = processor.get_train_examples(data_dir)
    return data
def get_user_bt_data(data_dir="data/train.csv"):
    processor = ClassificationProcessor()
    data = processor.get_train_bt_examples(data_dir)
    return data

if __name__ == "__main__":
    data = get_user_data('/data/mr/train.csv')
    contents_list = []
    for example in data:
        contents_list.append(example.contents)
    df = pd.DataFrame({'text': contents_list})
    df.to_csv('/data/mr/user_data_train.csv', index=False, header=False)