import pandas as pd
import numpy as np
import pickle

####################################
#  对工程返回模型处理完的数据
####################################
# 从csv的[0]位置获取数据，表示标签
def get_labels_from_csv(data_dir, save=False):
    """Gets a collection of `InputExample`s for the train set."""
    data = pd.read_csv(data_dir, header=None)
    if save:
        with open('data/labels_llm.npy', 'wb') as f:
            np.save(f, data[0].tolist())
            # print(len(data[0]))
            # print(len(data))
    return data[0].tolist()

# 从大模型输出路径中读取大模型标注数据
# list[map{id:id,Content:content,LLMlabel:label_list]
def get_llm_response(data_dir, shuffle_idx=None):
    data = pd.read_csv(data_dir, header=None)
    label_list = data[0].tolist()
    content_list = data[1].tolist()
    id_list = range(1, len(label_list)+1)
    response = [{'id': id_list[id], 'Content': content_list[idx], 'LLMLabel': label_list[idx]} for id, idx in enumerate(shuffle_idx)]
    return response
#  从小模型输出路径读取小模型数据，其中shuffle_idx还是必须传的参数
def get_slm_response(data_dir, shuffle_idx=None, refinery=False):
    data = pd.read_csv(data_dir, header=None)  # 路径中读取文件
    labels_llm = data[0].tolist()  # data[0] 是标签
    content_list = data[1].tolist()  # data[1] 与语料文本
    id_list = range(1, len(labels_llm)+1)  # id顺序编号
    if refinery:  # SLM精炼后的数据
        confidence_list = np.load('data/confidence_list_refinery.npy').tolist()  # 获取置信度的列表
        labels_slm = np.load('data/labels_slm_refinery.npy').tolist()  # 获取小模型标签列表
        rank_list = np.load('data/rank_list_refinery.npy').tolist()    # 获取 rank的列表
        demo_list = np.load('data/demo_list_refinery.npy').tolist()    # 获取 演示集demo的列表
    else:
        confidence_list = np.load('data/confidence_list.npy').tolist()  # 获取置信度的列表
        labels_slm = np.load('data/labels_slm.npy').tolist()  # 获取小模型标签列表
        rank_list = np.load('data/rank_list.npy').tolist()  # 获取 rank的列表
        demo_list = np.load('data/demo_list.npy').tolist()  # 获取 演示集demo的列表
    response = [{'id': id_list[id], 'Content': content_list[idx], 'LLMLabel': labels_llm[idx], 'SLMLabel': labels_slm[idx], 'Ranking': rank_list[idx], 'Confidence': confidence_list[idx], 'Demo': demo_list[idx]} for id, idx in enumerate(shuffle_idx)]
    return response 

#  获取散点数据
def get_scatter_data(shuffle_idx=None, refinery=False):
    if refinery:
        coordinates_list = np.load('data/coordinates_list_refinery.npy').tolist()  # 坐标列表
        labels_slm = np.load('data/labels_slm_refinery.npy').tolist()  # 小模型标签
    else:
        coordinates_list = np.load('data/coordinates_list.npy').tolist()
        labels_slm = np.load('data/labels_slm.npy').tolist()
    response = [[coordinates_list[idx][0], coordinates_list[idx][1], labels_slm[idx]] for idx in shuffle_idx]
    return response

# get_labels_from_csv('FreeAL-main/self_training_slm/data_in/mr/train.csv', save=True)

# 将NPY数据转出可读
def transform_npyfile_to_csvfile(original_data_dir, target_data_dir):

    datalist = np.load(original_data_dir).tolist()
    df = pd.DataFrame({'data': datalist})
    df.to_csv(target_data_dir, index=True, header=False)
    print("finished transform_npyfile_to_csvfile:",original_data_dir,target_data_dir)
    return
# 将PKL数据转出可读
def transform_pklfile_to_csvfile(original_data_dir, target_data_dir):
    with open(original_data_dir, "rb") as f:
        data = pickle.load(f)  
    df = pd.DataFrame({'data': data})
    df.to_csv(target_data_dir, index=True, header=False)
    print("finished transform_pklfile_to_csvfile:",original_data_dir,target_data_dir)
    return
# 比较训练数据准确率
# def cal_train_data_accuracy_rate():
#     accuracy_rate =0.00

#     return


if __name__ == "__main__":
   #transform_npyfile_to_csvfile("data/labels_slm.npy","data/labels_slm.csv")
    #transform_npyfile_to_csvfile("data/labels_slm_refinery.npy","data/labels_slm_refinery.csv")
    #transform_npyfile_to_csvfile("data/demo_list.npy","data/demo_list.csv")
    #transform_npyfile_to_csvfile("data/rank_list.npy","data/rank_list.csv")
    #transform_npyfile_to_csvfile("data/confidence_list.npy","data/confidence_list.csv")
    #transform_pklfile_to_csvfile("self_training_slm/feedback/pred_label_mr.pkl","self_training_slm/feedback/pred_label_mr.csv")
    transform_npyfile_to_csvfile("output_data/mr/mr_2th_SLM_labels_slm.npy","output_data/mr/mr_2th_SLM_labels_slm.csv")
    transform_npyfile_to_csvfile("output_data/mr/mr_4th_SLM_labels_slm.npy","output_data/mr/mr_4th_SLM_labels_slm.csv")