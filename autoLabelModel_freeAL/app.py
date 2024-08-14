from flask import Flask, jsonify
from flask import request
import os
import socket
import requests
from data_utils import *
from flask import url_for
import numpy as np
from flask_cors import CORS
import json
import csv
######
# 提供模型端的接口，提供处理完的数据返回
######
app = Flask(__name__)
# 大模型标注接口（实际同步调用shell脚本执行）
CORS(app, resources=r'/*')

shuffle_idx = np.random.permutation(8662)
# 大模型标注接口（实际同步调用shell脚本执行）
@app.route('/llm', methods=['GET', 'POST'])
def llm_labeling():
    if request.method == 'POST':
        f = request.files['file']
        data = pd.read_csv(f, header=None)
        global shuffle_idx
        shuffle_idx = np.random.permutation(len(data))
        filename = f.filename
        fullpath ="data/"+filename;
        np.savetxt(fullpath, data, delimiter=',', fmt='%s')
        # f.save(f'data/user_data_test.csv')
        # f.save(os.path.join('data/', 'user_data_.csv'))
        # filename=f.filename
        # with open(f'./{filename}','wb') as f2:
        #     f2.write(f.stream.read())
        
        #f.save('data/mr/user_data_.csv')
        # 打开文件进行写入
        # with open('data/output.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        # # 写入数据
        # for row in data:
        #     writer.writerow(row)

        response = jsonify({
                'code': '200',
                'message': 'Upload completed'
        })
        return response
    elif request.method == 'GET':
        if not os.path.exists('progress/llm_labeling_progress.json'):
            print('Start labeling with LLM')
            os.system("sh llm.sh")
            response = jsonify({
                'code': '201',
                'data': 0,
                'message': 'Start labeling'
            })
            return response
        else:
            with open('progress/llm_labeling_progress.json', 'r') as f:
                progress = json.load(f)
                if progress['current'] == progress['total']:
                    print('Labeling completed')
                    response = jsonify({
                        'code': '200',
                        'data': get_llm_response('data/mr/train.csv', shuffle_idx),
                        'message': 'Labeling completed'
                    })
                    return response
                else:
                    print('Continue labeling with LLM')
                    response = jsonify({
                        'code': '201',
                        'data': get_llm_response('data/mr/train.csv', shuffle_idx),
                        'message': 'Continue labeling',
                        'progress': progress['current'] / progress['total'] * 100
                    })
                    return response

    print('Labeling failed')
    response = jsonify({
        'code': '500',
        'message': 'Labeling failed'
    })
    return response

@app.route('/llm/refinery', methods=['GET'])
def llm_refinery():
    if request.method == 'GET':
        if not os.path.exists('progress/llm_refinery_progress.json'):
            print('Start refinery with LLM')
            os.system("sh llm_refinery.sh")
            response = jsonify({
                'code': '201',
                'data': 0,
                'message': 'Start refinery'
            })
            return response
        else:
            with open('progress/llm_refinery_progress.json', 'r') as f:
                progress = json.load(f)
                if progress['current'] == progress['total']:
                    print('Refinery completed')
                    response = jsonify({
                        'code': '200',
                        'data': get_llm_response('data/train_chat_llm_2.csv', shuffle_idx),
                        'message': 'Refinery completed'
                    })
                    return response
                else:
                    print('Continue refinery with LLM')
                    response = jsonify({
                        'code': '201',
                        'data': get_llm_response('data/mr/train.csv', shuffle_idx),
                        'message': 'Continue refinery',
                        'progress': progress['current'] / progress['total'] * 100
                    })
                    return response

    print('Refinery failed')
    response = jsonify({
        'code': '500',
        'message': 'Refinery failed'
    })
    return response
# 小模型筛选接口（实际同步调用shell脚本执行）
@app.route('/slm', methods=['GET'])
def slm_distilling():
    if request.method == 'GET':
        if not os.path.exists('progress/slm_training_progress.json'):
            print('Start training SLM')
            os.system("sh slm.sh")
            response = jsonify({
                'code': '201',
                'data': 0,
                'message': 'Start training'
            })
            return response
        else:
            with open('progress/slm_training_progress.json', 'r') as f:
                progress = json.load(f)
                if progress['current'] == progress['total']:
                    print('Training completed')
                    response = jsonify({
                        'code': '200',
                        'data': get_slm_response('data/mr/train.csv', shuffle_idx),
                        'message': 'Distilling completed',
                        'ScatterData': get_scatter_data(shuffle_idx)
                    })
                    return response
                else:
                    print('Continue training SLM')
                    response = jsonify({
                        'code': '201',
                        'data': progress['current'] / progress['total'] * 100,
                        'message': 'Continue training'
                    })
                    return response

    print('Distilling failed')
    response = jsonify({
        'code': '500',
        'message': 'Distilling failed'
    })
    return response

@app.route('/slm/refinery', methods=['GET'])
def slm_distilling_refinery():
    if request.method == 'GET':
        if not os.path.exists('progress/slm_training_progress.json'):
            print('Start training SLM')
            os.system("sh slm.sh")
            response = jsonify({
                'code': '201',
                'data': 0,
                'message': 'Start training'
            })
            return response
        else:
            with open('progress/slm_refinery_progress.json', 'r') as f:
                progress = json.load(f)
                if progress['current'] == progress['total']:
                    print('Training completed')
                    response = jsonify({
                        'code': '200',
                        'data': get_slm_response('data/mr/train.csv', shuffle_idx, True),
                        'message': 'Distilling completed',
                        'ScatterData': get_scatter_data(shuffle_idx, True)
                    })
                    return response
                else:
                    print('Continue training SLM')
                    response = jsonify({
                        'code': '201',
                        'data': progress['current'] / progress['total'] * 100,
                        'message': 'Continue training'
                    })
                    return response

    print('Distilling failed')
    response = jsonify({
        'code': '500',
        'message': 'Distilling failed'
    })
    return response
#  手动更新的数据上传到系统
@app.route('/manual', methods=['POST'])
def manual_labeling():
    if request.method == 'POST':
        data = request.json.get('manualOptions')
        data = np.array(list(map(int, data)))
        current_manual_label = np.array(np.load('data/labels_manual.npy'))
        # print(np.where(np.array(data) != -1)[0].astype(np.int64).dtype)
        current_manual_label[np.where(np.array(data) != -1)[0].astype(int)] = data[np.where(np.array(data) != -1)[0].astype(int)]
        np.save('data/labels_manual.npy', current_manual_label.tolist())
        if (os.system('sh manual.sh') == 0):
            response = jsonify({
                'code': '200',
                'message': 'Manual labeling completed'
            })
            print('Manual labeling completed')
            return response
        else:
            response = jsonify({
                'code': '500',
                'message': 'Manual labeling failed'
            })
            return response
    response = jsonify({
        'code': '500',
        'message': 'Manual labeling failed'
    })
    return response

# 提供展示结果
@app.route('/display', methods=['GET'])
def display():
    if request.method == 'GET':
        response = jsonify({
            'code': '200',
            'data': get_slm_response('data/mr/train.csv', shuffle_idx),
            'message': 'Distilling completed',
            'ScatterData': get_scatter_data(shuffle_idx)
        })
        return response

    response = jsonify({
        'code': '500',
        'message': 'Display failed'
    })
    return response
            
@app.route('/', methods=['GET', 'POST'])
def test():
    return 'Hello, world!'
            
if __name__ == '__main__':
    # res = requests.get('http://myip.ipip.net', timeout=5).text
    # print(res)
    app.run(host='0.0.0.0', port='5000')