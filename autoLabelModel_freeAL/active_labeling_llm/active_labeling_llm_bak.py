
import pickle
import argparse

import requests
import json
from data_utils import *
from tqdm import tqdm
# # llama3
# def ask_llama3(messages, model="llama3:8b"):
#     #stream_switch =False
#     url = "http://127.0.0.1:11434/api/chat"
#     payload = json.dumps({
#         "messages": messages,
#         "model": model,
#         "stream": False
#     })
#     headers = {
#         'Content-Type': 'application/json'
#     }
    
#     response = requests.request("POST", url, headers=headers, data=payload)
    
#     # print(response.text)
#     print(response.json()['message'])
    
#     return response.json()['message']['content']

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={key}"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def ask_Yiyan(messages, system="assistant"):
            
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    
    payload = json.dumps({
        "messages": messages,
        "sysyem": system
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    
    return response.json()["result"]

def slice_response(response):
    generatedSamples = []
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
    # response = ask_Yiyan(messages)
    response = "Here are 100 examples of labeled text for sentiment analysis on the MR (Movie Review) dataset:\n1. Positive: \"The movie is a refreshing take on the romantic comedy genre, with witty dialogue and charming performances.\"\n2. Negative: \"The plot is paper-thin and the acting is atrocious, making this movie a complete waste of time.\"\n3. Positive: \"A visually stunning film that captures the essence of the source material while adding its own unique flair.\"\n4. Negative: \"The characters are one-dimensional and the storyline is predictable, making this movie a snooze-fest.\"\n5. Positive: \"A heartwarming tale of friendship and redemption that will leave you with a smile on your face.\"\n6. Negative: \"The movie is let down by its sluggish pace and lack of engaging conflict.\"\n7. Positive: \"A thrilling action movie with breathtaking stunts and a pulse-pounding score.\"\n8. Negative: \"The dialogue is clunky and the plot holes are glaring, making this movie difficult to sit through.\"\n9. Positive: \"A charming coming-of-age story that captures the joys and heartaches of youth.\"\n10. Negative: \"The acting is wooden and the plot is convoluted, making this movie a chore to watch.\"\n...\nand so on, up to 100 examples. Please note that these are hypothetical examples and may not reflect actual movie reviews. However, they illustrate the kind of language and sentiment that might be found in positive and negative movie reviews."
    return slice_response(response)

def annotation_with_llm(userData, ICData, role="You are a helpful assistant for the task of text classification on the MR (Movie Review) dataset. You reply with brief, to-the-point answers with no elaboration as truthfully as possible. MR (Movie Review) dataset is used in sentiment-analysis experiments and this dataset contains moviereview documents labeled with respect to their overall sentiment polarity (positive or negative). Your task is to a binary classification to classify a movie review as positive or negative according to their overall sentiment polarity. The category is divided into two types: ’positive’ and ’negative’.", instruction="Given a movie review, how do you feel about the sentiment polarity of the given movie review, is this positive or negative? Please answer in a single line with ’positive’ or ’negative’. You must answer with ’positive’ or ’negative’, do not answer anything else."):
    idx = 0
    for sample in tqdm(userData[:3]):
        if args.refinery and idx in right_list_all:
            label = str(pred_labels[idx])
            idx += 1
            label_list.append(label)
            content_list.append(sample.contents)
            continue
        messages = []
        # for example in ICData[:10]:
        for example in top_indices[idx]:
            messages.append({"role": "user", "content": instruction + userData[example].contents})
            messages.append({"role": "assistant", "content": "positive" if userData[example].label else "negative"})
        initial_tag = True
        label_list = []
        content_list = []
        
        temp_messages = messages.copy()
        temp_messages.append({"role": "user", "content": instruction + sample.contents})
        # print(temp_messages)
        response = ask_Yiyan(messages=temp_messages, system=role)
        if response[-1] == '.':
                response = response[:-1]
        if response.lower() == "negative":
            label = '0'
        elif response.lower() == "positive":
            label = '1'
        else:
            label = '-1'
        
        idx += 1
        
        label_list.append(label)
        content_list.append(sample.contents)

    # save annotated dataset to .csv file
    df = pd.DataFrame({'label': label_list, 'text': content_list})
    df.to_csv('/data/home/Lin_Long/VLDB_Demo/data/mr/train_.csv', index=False, header=False)


parser = argparse.ArgumentParser()
parser.add_argument("--refinery", action="store_true", default=False)
args = parser.parse_args()

with open("../self_training_slm/feedback/right_list_mr.pkl", "rb") as f:
    right_list_all = pickle.load(f)  # clean sample idx

with open("../self_training_slm/feedback/demo_index_mr.pkl", "rb") as f:
    top_indices = pickle.load(f)  # demonstration retrieval by SLM's embeddings
    
with open("../self_training_slm/feedback/pred_label_mr.pkl", "rb") as f:
    pred_labels = pickle.load(f)  # pseudo-labels by SLM

userData = get_user_data('/data/home/Lin_Long/VLDB_Demo/data/mr/user_data.csv')
generatedSamples = get_self_generated_samples(unlabeled_set=userData)
annotation_with_llm(userData=userData, ICData=generatedSamples)
