import numpy as np
import pickle
from active_labeling_llm.data_utils import get_user_data
import pandas as pd
##################
# 处理手动更正数据脚本
##################
# 加载npy手动更正数据的脚本
#manual_label = np.load('data/labels_manual.npy').tolist()
manual_label = np.load('data/labels_manual.npy').tolist()

# 获取用户提交的更正数据
#userData = get_user_data('data/mr/user_data.csv')
userData = get_user_data('data/mr/manual_label_demo.csv')

label_list = []
content_list = []

for example in userData:
    label_list.append(example.label)
    content_list.append(example.contents)
# 保存长度
len_label_list=len(label_list)
len_content_list=len(content_list)

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
    label_list[idx] = label
        
with open("self_training_slm/feedback/right_list_mr_.pkl", "wb") as f:
    pickle.dump(right_list_all, f)

with open("self_training_slm/feedback/pred_label_mr_.pkl", "wb") as f:
    pickle.dump(pred_labels, f)
    
df = pd.DataFrame({'label': label_list, 'text': content_list})
df.to_csv('data/mr/train__.csv', index=False, header=False)
print("finished!")

def manual_update():
    return None

if __name__ == "__main__":
    manual_update()