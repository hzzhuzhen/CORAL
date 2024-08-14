import os
import numpy as np
import pickle
from active_labeling_llm.data_utils import get_user_data
import pandas as pd

manual_label = []
userData = []
#manual_label = np.load('data/labels_manual.npy').tolist()
LABELS_MANUAL_NPY_PATH='data/manual_label.npy'
LABELS_MANUAL_CSV_PATH='data/manual_label.csv'
USER_MANUAL_LABEL_PATH='data/mr/manual_label_demo.csv'
USER_TRAIN_PATH='data/mr/train_demo.csv'
if os.path.exists(USER_TRAIN_PATH):
    userData_train_csv = get_user_data(USER_TRAIN_PATH)  # 用户标注的CSV的文件
if os.path.exists(LABELS_MANUAL_NPY_PATH):
    manual_label = np.load(LABELS_MANUAL_NPY_PATH).tolist() # 人工更正的NPY文件
if os.path.exists(USER_MANUAL_LABEL_PATH):
    userData_ml_csv = get_user_data(USER_MANUAL_LABEL_PATH)  # 用户标注的CSV的文件

# 如何历史manual_label不存在，则构建一个默认值为-1，长度和train数据等长
manual_label =np.full(len(userData_train_csv),-1)
    
ml_label_list = []
ml_content_list = []


for example in userData_ml_csv:
    ml_label_list.append(example.label)
    ml_content_list.append(example.contents)
# 保存长度
len_label_list=len(ml_label_list)
len_content_list=len(ml_content_list)

with open("self_training_slm/feedback/right_list_mr.pkl", "rb") as f:
    right_list_all = pickle.load(f)  # clean sample idx

with open("self_training_slm/feedback/demo_index_mr.pkl", "rb") as f:
    top_indices = pickle.load(f)  # demonstration retrieval by SLM's embeddings
    
with open("self_training_slm/feedback/pred_label_mr.pkl", "rb") as f:
    pred_labels = pickle.load(f)  # pseudo-labels by SLM

for idx, label in enumerate(manual_label):
    if label == -1:
        continue
    # 过滤掉多余的数据
    if (idx > len_label_list) or (idx > len_content_list):
        continue    
    if idx not in right_list_all:
        right_list_all.append(idx)
    pred_labels[idx] = label
    ml_label_list[idx] = label
        
with open("self_training_slm/feedback/right_list_mr_.pkl", "wb") as f:
    pickle.dump(right_list_all, f)

with open("self_training_slm/feedback/pred_label_mr_.pkl", "wb") as f:
    pickle.dump(pred_labels, f)
    
df = pd.DataFrame({'label': ml_label_list, 'text': ml_content_list})
df.to_csv(LABELS_MANUAL_CSV_PATH, index=False, header=False)
# 保存到.npy文件
np.save(LABELS_MANUAL_NPY_PATH, manual_label)
print("finished!")

def manual_update_new():
    return None

if __name__ == "__main__":
    manual_update_new()