import os
from active_labeling_llm.data_utils import get_user_data,get_user_bt_data
import pandas as pd
######################
## 生成SLM input数据
######################

LLM_OUTPUT_PATH='data/mr/train_.csv'
SLM_TARGET_TRAIN_DATA_PATH='data/mr/train_chat_bt.csv'
TEMPLATE_TRAIN_DATA_PATH = 'data/mr/train_chat_bt_template.csv'
def prepare_train_data_for_slm():
    if os.path.exists(LLM_OUTPUT_PATH):
        llm_output_csv = get_user_data(LLM_OUTPUT_PATH)
    if os.path.exists(TEMPLATE_TRAIN_DATA_PATH):  
        template_train_data_csv = get_user_bt_data(TEMPLATE_TRAIN_DATA_PATH) 

    label_list = []
    content_list = []
    content_bt_list =[]
    new_label_list =[]
    new_content_list = []
    new_content_bt_list =[]
    for template in template_train_data_csv:
        label_list.append(template.label)
        content_list.append(template.contents)
        content_bt_list.append(template.contents_bt)
    for example in llm_output_csv:
        new_label_list.append(example.label)
        new_content_list.append(example.contents)
        for idx,content in enumerate(content_list):
            if content == example.contents:
                new_content_bt_list.append(content_bt_list[idx])
                break

    df = pd.DataFrame({'label': new_label_list,'content_list': new_content_list,'content_bt_list': new_content_bt_list})
    df.to_csv(SLM_TARGET_TRAIN_DATA_PATH, index=False, header=False)
    print("finished!")
    return

if __name__ == "__main__":
    prepare_train_data_for_slm()