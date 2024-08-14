import os
import numpy as np
import pickle
from active_labeling_llm.data_utils import get_user_data
import pandas as pd
#############################################################
## 手动打乱数据
############################################################


userData = []
TRAIN_PATH='data/mr/train.csv'
TRAIN_PATH_SHUFFLE='data/mr/train_shuffle.csv'
USER_MANUAL_LABEL_PATH='data/mr/user_data.csv'

def manual_shuffle():
    if os.path.exists(TRAIN_PATH):
        train_csv = get_user_data(TRAIN_PATH)  # 基准训练数据
    label_list = []
    content_list = []

    for example in train_csv:
        label_list.append(example.label)
        content_list.append(example.contents)

    df = pd.DataFrame({'label': label_list,'content':content_list})
    # 假设df是你的DataFrame
    df = df.sample(frac=1).reset_index(drop=True)
    print(label_list)
    df.to_csv(TRAIN_PATH_SHUFFLE, index=False, header=False)
    df2 = pd.DataFrame({'content':content_list})
    df2.to_csv(USER_MANUAL_LABEL_PATH, index=False, header=False)    
    print("finished!")
    return



if __name__ == "__main__":
    manual_shuffle()