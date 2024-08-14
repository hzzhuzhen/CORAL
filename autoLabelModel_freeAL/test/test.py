import numpy as np


manual_label =np.full(100,1)
print(manual_label.shape)
new_list= np.zeros(100)
new_list[1]=1
print(new_list.shape)
#print(new_list2.shape)
new_list[np.int64(np.where(manual_label == 1)[0])] = manual_label[np.int64(np.where(manual_label == 1))]
print(manual_label[np.int64(np.where(manual_label == 1))])
print(np.int64(np.where(manual_label == 1)[0]))
print(new_list)

    #测试代码
    # new_manual_label = manual_label
    # new_manual_label[np.int64(np.where(manual_label == -1)[0])] = manual_label[np.int64(np.where(manual_label == -1))]
    # print("ok")