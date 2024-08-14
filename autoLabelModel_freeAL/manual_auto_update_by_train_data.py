import os
import numpy as np
import pickle
from active_labeling_llm.data_utils import get_user_data
import pandas as pd
#############################################################
## 脚本模拟人工对低置信度/低rank的数据做标注
## 标注数量由阈值(threadhold)控制,默认5%的数据
############################################################
auto_update_method ="confidence"
#auto_update_method ="rank"
#auto_update_method ="human"
manual_label = []
userData = []
#manual_label = np.load('data/labels_manual.npy').tolist()
TRAIN_PATH='data/mr/train.csv'
USER_MANUAL_LABEL_PATH='data/mr/user_data.csv'
CONFIDENCE_LIST_PATH='data/confidence_list.npy'
RANK_LIST_PATH='data/rank_list.npy'
LABELS_MANUAL_NPY_PATH='data/manual_label.npy'
LABELS_MANUAL_CSV_PATH='data/manual_label.csv'
def manual_auto_update_new():
    if os.path.exists(TRAIN_PATH):
        train_csv = get_user_data(TRAIN_PATH)  # 基准训练数据
    if os.path.exists(LABELS_MANUAL_NPY_PATH):
        manual_label = np.load(LABELS_MANUAL_NPY_PATH).tolist() # 人工更正的NPY文件
    if os.path.exists(USER_MANUAL_LABEL_PATH):
        userData_ml_csv = get_user_data(USER_MANUAL_LABEL_PATH)  # 用户标注的CSV的文件
    if os.path.exists(CONFIDENCE_LIST_PATH):
        confidence_list = np.load(CONFIDENCE_LIST_PATH)  # 置信度数据
    if os.path.exists(RANK_LIST_PATH):
        rank_list = np.load(RANK_LIST_PATH)  # rank的数据
    # 如何历史manual_label不存在，则构建一个默认值为-1，长度和train数据等长
    manual_label =np.full(len(train_csv),-1)
        
    auto_manual_label_num = len(userData_ml_csv)*0.05
    auto_manual_label_num = np.int64(np.round(auto_manual_label_num) )#人工标注量取5%


    if auto_update_method=='confidence':
        print(confidence_list)   
        for seq in range(1,auto_manual_label_num):
            index_of_min = np.argmin(confidence_list)
            target_label = train_csv[index_of_min].label #csv读出来的数据都是从0开始，在excel和文档展示的时候是从1开始
            manual_label[index_of_min] = target_label
            original_configdence_value= confidence_list[index_of_min]
            confidence_list[index_of_min] = 1.0
            print("基于低置信度准则标注:标注次数|数据序号|原置信度| 新标注标签",seq,index_of_min,original_configdence_value,target_label)
        print(manual_label)   

    elif  auto_update_method =='rank':
        print(rank_list)   
        for seq in range(1,auto_manual_label_num):
            index_of_min = np.argmax(rank_list)
            target_label = train_csv[index_of_min].label
            manual_label[index_of_min] = target_label
            original_rank_value = rank_list[index_of_min]
            rank_list[index_of_min] = seq-auto_manual_label_num
            print("基于高排座位准则标注:标注次数| 数据序号|原排序值| 新标注标签",seq,index_of_min,original_rank_value,target_label)
        print(manual_label)      
    else:
        print("no match method!")  
        return 
    # 保存长度
    len_new_manual_label = len(manual_label)

    with open("self_training_slm/feedback/right_list_mr.pkl", "rb") as fmu:
        right_list_all = pickle.load(fmu)  # clean sample idx

    with open("self_training_slm/feedback/demo_index_mr.pkl", "rb") as fmu:
        top_indices = pickle.load(fmu)  # demonstration retrieval by SLM's embeddings
        
    with open("self_training_slm/feedback/pred_label_mr.pkl", "rb") as fmu:
        pred_labels = pickle.load(fmu)  # pseudo-labels by SLM

    for idx, label in enumerate(manual_label):
        if label == -1:
            continue
        # 过滤掉多余的数据
        if (idx > len_new_manual_label) or (idx == len_new_manual_label):
            continue    
        if idx not in right_list_all:
            right_list_all.append(idx)
        if label != pred_labels[idx]:
            pred_labels[idx] = label

    with open("self_training_slm/feedback/right_list_mr.pkl", "wb") as f:
        pickle.dump(right_list_all, f)

    with open("self_training_slm/feedback/pred_label_mr.pkl", "wb") as f:
       pickle.dump(pred_labels, f)
        
    df = pd.DataFrame({'label': manual_label})
    df.to_csv(LABELS_MANUAL_CSV_PATH, index=False, header=False)
    # 保存到.npy文件
    np.save(LABELS_MANUAL_NPY_PATH, manual_label)
    print("finished!")
    return



if __name__ == "__main__":
    manual_auto_update_new()