import os
#import backoff  # for exponential backoff
import pandas as pd
import numpy as np
import re
import pickle
import argparse
#import openai
#import openai_manager
#from openai.embeddings_utils import get_embedding, cosine_similarity
import requests
import json
from data_utils import *
from tqdm import tqdm
import data_utils

# Your API key (ChatGPT)
# openai_manager.append_auth_from_config(config_path="openai_api_config.yml")


# @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
# def get_embedding_backoff(*args, **kwargs):
#     return get_embedding(*args, **kwargs)

# Setup for Yiyan 文心一言
def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    # longling account    
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Q5vv5n6ebmRfhfBiH4tQuicH&client_secret=r0sfV62QfDWeyRKWAZYpHQF0VX84Odrp"
    # rogerzzhu account  
    #url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GjkHsZ7CwmrafbKZCudrmRZK&client_secret=4fmMdBlHfE7ndjPft0g3V1QzvGja7qXv"   
    #url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=QQIoGzqwS6JIJ0G9yTqSmllB&client_secret=T7Sf6eZk6jqMzHh7Kk08ejlBG4iEJKAB"

    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def ask_Yiyan(messages, system="assistant"):

    # 文心一言4.0        
    #url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    # tiny-8K maybe free
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-tiny-8k?access_token=" + get_access_token()
    #Lite-8k
    #url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": messages,
        "system": system
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    
    return response.json()["result"]
# llama3
def ask_llama3(messages, model="llama3:8b"):

    #stream_switch =False
    url = "http://127.0.0.1:11434/api/chat"
    payload = json.dumps({
        "messages": messages,
        "model": model,
        "stream": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    print(response.json()['message'])
    
    return response.json()['message']['content']
# def askLlama3(messages):
#     MODEL = "llama3:8b"
#     response = openai_manager.ChatCompletion.create(model=MODEL, messages=messages, n=1)
#     return response


def slice_response(response):
    generatedSamples = []
    # slice the response by line, and if a line starts with a number, then insert a DatasetInputExample element into generatedSamples, if the first word between the starting number and the first ':' was 'positive', then the label is 1, otherwise 0, the 'contetnt' field is the contents inside the ""
    lines = response.split('\n')
    for line in lines:
        if line[0].isdigit():
            label = 1 if line[line.index('.') + 2].lower() == 'p' else 0
            content = line[line.index('"') + 1: line.rindex('"')]
            generatedSamples.append(DatasetInputExample(contents=content, label=label, contents_bt=None))
    return generatedSamples
    
def get_self_generated_samples(unlabeled_set, instruction="You are required to produce 100 English examples with labels for the task of text classification on the MR (Movie Review) dataset. These samples will be used as prompt examples for the GPT model. MR dataset is used in sentiment-analysis experiments and this dataset contains moviereview documents labeled with respect to their overall sentiment polarity (positive or negative). The task is to classify a movie review as positive or negative according to their overall sentiment polarity. For example, 100 of the unlabeled samples in MR dataset are as follows:"):
    prompt = instruction + " For example, 100 of the unlabeled samples in the dataset are as follows:" 
    for sample in unlabeled_set[:100]:
        prompt += " [" + sample.contents + "]"
    messages = [{"role": "user", "content": prompt}]
    # call remote LLM for samples
    #response = ask_Yiyan(messages)
    # use former generated response 直接利用生成好的结果
    response = "Here are 100 examples of labeled text for sentiment analysis on the MR (Movie Review) dataset:\n1. Positive: \"The movie is a refreshing take on the romantic comedy genre, with witty dialogue and charming performances.\"\n2. Negative: \"The plot is paper-thin and the acting is atrocious, making this movie a complete waste of time.\"\n3. Positive: \"A visually stunning film that captures the essence of the source material while adding its own unique flair.\"\n4. Negative: \"The characters are one-dimensional and the storyline is predictable, making this movie a snooze-fest.\"\n5. Positive: \"A heartwarming tale of friendship and redemption that will leave you with a smile on your face.\"\n6. Negative: \"The movie is let down by its sluggish pace and lack of engaging conflict.\"\n7. Positive: \"A thrilling action movie with breathtaking stunts and a pulse-pounding score.\"\n8. Negative: \"The dialogue is clunky and the plot holes are glaring, making this movie difficult to sit through.\"\n9. Positive: \"A charming coming-of-age story that captures the joys and heartaches of youth.\"\n10. Negative: \"The acting is wooden and the plot is convoluted, making this movie a chore to watch.\"\n...\nand so on, up to 100 examples. Please note that these are hypothetical examples and may not reflect actual movie reviews. However, they illustrate the kind of language and sentiment that might be found in positive and negative movie reviews."
    print("samples:",response)
    return slice_response(response)

def annotation_with_llm(args, userData, ICData,manual_labels, role="You are a helpful assistant for the task of text classification on the MR (Movie Review) dataset. You reply with brief, to-the-point answers with no elaboration as truthfully as possible. MR (Movie Review) dataset is used in sentiment-analysis experiments and this dataset contains moviereview documents labeled with respect to their overall sentiment polarity (positive or negative). Your task is to a binary classification to classify a movie review as positive or negative according to their overall sentiment polarity. The category is divided into two types: ’positive’ and ’negative’.", instruction="Given a movie review, how do you feel about the sentiment polarity of the given movie review, is this positive or negative? Please answer in a single line with ’positive’ or ’negative’. You must answer with ’positive’ or ’negative’, do not answer anything else.", test=True):
    idx = 0
    # 只用3条数据
    #annotationNumber = 3 if test else len(userData)
    # 用真实数据标注
    annotationNumber = len(userData) #暂时用真实的数据跑一波标注
    
    label_list = []
    content_list = []
    if args.refinery:
        with open("../self_training_slm/feedback/right_list_mr.pkl", "rb") as fi:
            right_list_all = pickle.load(fi) # 选中正确的列表
        with open("../self_training_slm/feedback/demo_index_mr.pkl", "rb") as fi:
            top_indices = pickle.load(fi)  # demonstration retrieval by SLM's embeddings
        with open("../self_training_slm/feedback/pred_label_mr.pkl", "rb") as fi:
            pred_labels = pickle.load(fi)  # pseudo-labels by SLM

    labeled_llm =[]
    if args.rerun_labeling:
        if os.path.exists("../data/mr/train_old.csv"):
            labeled_llm = get_user_data("../data/mr/train_old.csv")

    for sample in tqdm(userData[:annotationNumber]):
        if args.rerun_labeling:
            oldlabel=labeled_llm[idx].label
            if oldlabel!= -1:
                label_list.append(oldlabel)
                content_list.append(sample.contents)
                idx += 1
                continue

        if args.refinery and idx in right_list_all:
            label = str(pred_labels[idx])
            idx += 1
            label_list.append(label)
            content_list.append(sample.contents)
            continue
        # 有人工标注数据，强制转成人工标注数据(和上面效果相同，防遗漏)
        if args.refinery and manual_labels.size>0 and manual_labels[idx]>-1:
            label = str(manual_labels[idx])
            idx += 1
            label_list.append(label)
            content_list.append(sample.contents)
            print("将遗漏的人工标签数据加入结果")
            continue
        messages = []
        if args.refinery:
            for example in top_indices[idx]: # SLM精练出来的演示集
                messages.append({"role": "user", "content": instruction + userData[example].contents})
                messages.append({"role": "assistant", "content": "positive" if userData[example].label else "negative"})
        else:
            for example in ICData: # 首次prompt自动生成的演示集
                messages.append({"role": "user", "content": instruction + example.contents})
                messages.append({"role": "assistant", "content": "positive" if example.label else "negative"})
        
        temp_messages = messages.copy()
        temp_messages.append({"role": "user", "content": instruction + sample.contents})

        #response = ask_Yiyan(messages=temp_messages, system=role)
        try:
            #response = ask_Yiyan(messages=temp_messages, system=role)
            response = ask_llama3(messages=temp_messages)
        except Exception as ex:
            error_message = " An exception of ask LLM occurred. temp_messages={0},{1},error_message={2}"
            print(error_message.format(type(ex).__name__),ex.args,temp_messages)
            response = 'excetion occured.' # 传入默认值        
        if response[-1] == '.':
                response = response[:-1]
        if response.lower() == "negative":
            label = '0'
        elif response.lower() == "positive":
            label = '1'
        else:
            print("It can not match any label so defined as -1:",response)
            label = '-1'
        idx += 1
        label_list.append(label)
        content_list.append(sample.contents)
        
        progress = {
            'current': idx,
            'total': annotationNumber
        }
        if args.refinery:
            with open('../progress/llm_refinery_progress.json', 'w') as f:
                json.dump(progress, f)
        else:
            with open('../progress/llm_labeling_progress.json', 'w') as f:
                json.dump(progress, f)
        
        # save annotated dataset to .csv file
        df = pd.DataFrame({'label': label_list, 'text': content_list})
        df.to_csv('../data/mr/train_.csv', index=False, header=False)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refinery", action="store_true", default=False) #带上是否精练的标签
    parser.add_argument("--rerun_labeling", action="store_true", default=False) #使用重标注，需要先将数据拷贝到同目录的trian_old
    args = parser.parse_args()
    manual_labels=[]
    if args.refinery:
        with open("../self_training_slm/feedback/right_list_mr.pkl", "rb") as fo:
            right_list_all = pickle.load(fo)  # clean sample idx

        with open("../self_training_slm/feedback/demo_index_mr.pkl", "rb") as fo:
            top_indices = pickle.load(fo)  # demonstration retrieval by SLM's embeddings
            
        with open("../self_training_slm/feedback/pred_label_mr.pkl", "rb") as fo:
            pred_labels = pickle.load(fo)  # pseudo-labels by SLM
        if os.path.exists("../data/manual_label.npy"):
            with open("../data/manual_label.npy", "rb") as f:
                manual_label_file_data = np.load(f)
                if manual_label_file_data.size > 0:
                    manual_labels = manual_label_file_data
                    

    #userData = get_user_data('../data/mr/user_data.csv')
    #userData = get_user_data('../data/test.csv') #先切换成少的
    userData = get_user_data('../data/mr/user_data.csv') #正式训练数据
    generatedSamples = None
    # 非LLM refinery 则生成初始演示集
    if not args.refinery:
        generatedSamples = get_self_generated_samples(userData)
        
    annotation_with_llm(args, userData, generatedSamples,manual_labels)

# ---------------------- test -----------------------
# messages = [{"role": "user", "content": "What is the capital of France?"}]
# askYiyan(messages)

# ----------------- active labeling -----------------

if __name__ == '__main__':
    main()
    # temp_messages = []
    # temp_messages.append({"role": "user", "content": "the movies is terrible. response the motion is negtivate or postive"})
    # ask_llama3(temp_messages)


# # embedding of self-generated demonstrations
# df = pd.read_csv("embedding/embedding_mr_gen.csv")
# df["embeddings"] = df.embeddings.apply(eval).apply(np.array)
# # embedding of the unlabeled training dataset
# df_train = pd.read_csv("embedding/embedding_mr_train.csv")
# df_train["embeddings"] = df_train.embeddings.apply(eval).apply(np.array)

# if args.refinery:
#     print("in refinery annotation")
#     with open("../self_training_slm/feedback/right_list_mr.pkl", "rb") as f:
#         right_list_all = pickle.load(f)  # clean sample idx

#     with open("../self_training_slm/feedback/demo_index_mr.pkl", "rb") as f:
#         top_indices = pickle.load(f)  # demonstration retrieval by SLM's embeddings

#     with open("../self_training_slm/feedback/pred_label_mr.pkl", "rb") as f:
#         pred_labels = pickle.load(f)  # pseudo-labels by SLM
# else:
#     print("in initial annotation")
# start_idx = 0
# test_num = len(df_train) - start_idx
# sel_list = range(start_idx, start_idx + test_num)
# df_train = df_train.iloc[sel_list].reset_index(drop=True)
# all_text = df_train["text"]
# all_embeddings = df_train["embeddings"]


# def askChatGPT(messages):
#     MODEL = "gpt-3.5-turbo"
#     response = openai_manager.ChatCompletion.create(model=MODEL, messages=messages, n=1)
#     return response


# # search in-context
# def search_intext(embedding, n=3):
#     query_embedding = embedding
#     df["similarity"] = df.embeddings.apply(
#         lambda x: cosine_similarity(x, query_embedding)
#     )
#     results = df.sort_values("similarity", ascending=False, ignore_index=True)
#     intext_results = results.head(n)
#     return intext_results

# all_response = []
# all_sentences = []
# batch_messages = []
# batch_sentences = []
# batch_index = []
# count = 0
# initial_tag = True
# for i in sel_list:
#     n = 10
#     sentence = all_text[i]
#     embedding = all_embeddings[i]
#     if not args.refinery:
#         # initial round: retrieval by bert embeddings
#         intext_results = search_intext(embedding, n)
#     else:
#         # refinery round: retrieval by SLM
#         ds_examples = df_train.iloc[top_indices[i]].reset_index(drop=True)
#         ds_annos = [pred_labels[idx] for idx in top_indices[i]]

#     sentence = sentence.replace('"', '"').replace("\n", "")
#     sentence_to_chatgpt = "Given a movie review: '" + sentence + "'"

#     sentences_example = []
#     annos_example = []
#     temp_messages = [
#         {
#             "role": "system",
#             "content": "You are a helpful assistant for the task of text classification on the MR (Movie Review) dataset. You reply with brief, to-the-point answers with no elaboration as truthfully as possible. MR (Movie Review) dataset  is used in sentiment-analysis experiments and this dataset contains movie-review documents labeled with respect to their overall sentiment polarity  (positive or negative). Your task is to a binary classification to classify a movie review as positive or negative according to their overall sentiment polarity. The category is divided into two types: 'positive' and 'negative'.",
#         },
#     ]
#     for j in range(n):
#         if args.refinery:
#             temp_sentence = (
#                 ds_examples.iloc[j]["text"].replace("\n", "").replace('"', '"')
#             )
#             temp_anno = "positive" if (ds_annos[j]) else "negative"
#         else:
#             temp_sentence = (
#                 intext_results.iloc[j]["text"].replace("\n", "").replace('"', '"')
#             )
#             temp_anno = intext_results.iloc[j]["anno"]
#         sentences_example.append(temp_sentence)
#         annos_example.append(temp_anno)
#         temp_messages.append(
#             {"role": "user", "content": "Given a movie review: '" + temp_sentence + "'"}
#         )
#         temp_messages.append(
#             {
#                 "role": "user",
#                 "content": "How do you feel about the sentiment polarity of the given movie review, is this positive or negative? please answer in a single line with 'positive' or 'negative'. You must answer with 'positive' or 'negative', do not answer anything else.",
#             }
#         )
#         temp_messages.append({"role": "assistant", "content": temp_anno})

#     temp_messages.append({"role": "user", "content": sentence_to_chatgpt})
#     temp_messages.append(
#         {
#             "role": "user",
#             "content": "How do you feel about the sentiment polarity of the given movie review, is this positive or negative? please answer in a single line with 'positive' or 'negative'. You must answer with 'positive' or 'negative', do not answer anything else.",
#         }
#     )
#     # print(temp_messages)
#     batch_index.append(i)
#     batch_messages.append(temp_messages)
#     batch_sentences.append(sentence)
#     count += 1
#     if (
#         count == 100
#     ):  # set a budget to reduce the negative impact of exceptions in annotations
#         response = askChatGPT(batch_messages)
#         all_response += response
#         all_sentences += batch_sentences
#         for i in range(len(batch_sentences)):
#             final_anno = response[i]["choices"][0]["message"]["content"]
#             if final_anno[-1] == ".":
#                 final_anno = final_anno[:-1]
#             if final_anno.lower() == "negative":
#                 final_label = "0"
#             elif final_anno.lower() == "positive":
#                 final_label = "1"
#             else:
#                 final_label = "-1"
#             if args.refinery and batch_index[i] in right_list_all:
#                 final_label = str(pred_labels[batch_index[i]])
#             if initial_tag:
#                 with open("results/output_mr_train.txt", "w") as f_out:
#                     f_out.write(final_label + "\n")
#                     initial_tag = False
#             else:
#                 with open("results/output_mr_train.txt", "a") as f_out:
#                     f_out.write(final_label + "\n")

#         batch_messages = []
#         batch_sentences = []
#         batch_index = []
#         count = 0
# if len(batch_messages):
#     response = askChatGPT(batch_messages)
#     all_response += response
#     all_sentences += batch_sentences
#     for i in range(len(batch_sentences)):
#         final_anno = response[i]["choices"][0]["message"]["content"]
#         if final_anno[-1] == ".":
#             final_anno = final_anno[:-1]
#         if final_anno.lower() == "negative":
#             final_label = "0"
#         elif final_anno.lower() == "positive":
#             final_label = "1"
#         else:
#             final_label = "-1"
#         if args.refinery and batch_index[i] in right_list_all:
#             # clean samples do not require reannotation
#             final_label = str(pred_labels[batch_index[i]])

#         if initial_tag:
#             with open("results/output_mr_train.txt", "w") as f_out:
#                 f_out.write(final_label + "\n")
#                 initial_tag = False
#         else:
#             with open("results/output_mr_train.txt", "a") as f_out:
#                 f_out.write(final_label + "\n")
