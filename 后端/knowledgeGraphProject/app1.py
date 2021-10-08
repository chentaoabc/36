from flask import Flask, request, jsonify
from flask_cors import *
import json,time
from py2neo import Graph, NodeMatcher
import networkx as nx
import pandas as pd
from default import NODE_COLOR, LINE_STYLE, NEIGHBOR_NUM
from creat import get_newdata,creat_node
from subprocess import *
import subprocess
import  threading

# # 连接图数据库
# G = Graph("http://neo4jdata.lingbtech.com:7474/browser/", auth=('neo4j', 'ct012345678'))
# node_matcher = NodeMatcher(G)
# #
G = Graph("bolt://localhost:7687", auth=('neo4j', 'ct123456'))
node_matcher = NodeMatcher(G)

proc=subprocess.Popen(['python','creat.py'],shell=True)
proc1=subprocess.Popen(['python','creat.py'],shell=True)



# 设置连边颜色
def make_line_style(source, target):
    if source == '信号' and target == '信号':
        line_style = LINE_STYLE['signal_with_signal']
    elif source == '干扰' and target == '干扰':
        line_style = LINE_STYLE['noise_with_noise']
    else:
        line_style = LINE_STYLE['signal_with_noise']
    return line_style


# 制作根节点json数据格式
def make_root(node_name):
    root_node = (pd.DataFrame(node_matcher.match(name=node_name))).to_dict()
    root_id = int(root_node['name'][0][2:])
    root_attributes = {}
    # 根节点为信号
    if root_node['name'][0][0:2] == '信号':
        root_id = -root_id
        root_label = '信号(%s)' % (root_node['Modulation_method'][0])
        root_color = NODE_COLOR[root_node['Modulation_method'][0]]
    # 根节点为干扰
    elif root_node['name'][0][0:2] == '干扰':
        root_label = '干扰(%s)' % (root_node['Interference_method'][0])
        root_color = NODE_COLOR[root_node['Interference_method'][0]]
    else:
        root_label = 'error'
        root_color = 'error'
    for key in root_node:
        if key != 'name' and key != 'id':
            root_attributes[key] = root_node[key][0]
    return {
        'id': root_id,
        'label': root_label,
        'name': node_name,
        'color': root_color,
        'attributes': root_attributes,
        'categary': '百科',
        'children': None
    }


# 制作邻居节点json数据格式
def make_child_json(root_node_name, child_attribute, child_categary):
    child_name = child_attribute['name']
    child_id = int(child_attribute['name'][2:])
    if child_name[0:2] == '信号':
        child_id = -child_id
        child_label = '信号(%s)' % (child_attribute['Modulation_method'])
        child_color = NODE_COLOR[child_attribute['Modulation_method']]
    else:
        child_label = '干扰(%s)' % (child_attribute['Interference_method'])
        child_color = NODE_COLOR[child_attribute['Interference_method']]
    del child_attribute['name']
    return {
        'id': child_id,
        'label': child_label,
        'name': child_name,
        'color': child_color,
        'attributes': child_attribute,
        'categary': child_categary,
        'lineStyle': make_line_style(root_node_name, child_name[0:2])
    }


# 制作邻居节点json数据格式
def make_child(node_name):
    children = []
    if node_name[0:2] == '信号':
        # 信号与信号
        match_code = "MATCH(a) - [b:信号相似] - (c {name:'%s'}) Return a,b ORDER BY b.Signal_similarity_ratio DESC LIMIT %d" % \
                     (node_name, NEIGHBOR_NUM)
        neighbors = pd.DataFrame(G.run(match_code))
        if not neighbors.empty:
            for i in range(neighbors.shape[0]):
                child_attribute = {}
                root_node_name = node_name[0:2]
                for key in neighbors[0][i]:
                    child_attribute[key] = neighbors[0][i][key]
                child_categary = '信号相似度: %s' % (str(round(neighbors[1][i]['Signal_similarity_ratio'], 4)))
                children.append(make_child_json(root_node_name, child_attribute, child_categary))
        # 信号与干扰
        match_code = "MATCH(a) - [b:误码率] - (c {name:'%s'}) Return a,b ORDER BY b.error_rate DESC LIMIT %d" % \
                     (node_name, NEIGHBOR_NUM)
        neighbors = pd.DataFrame(G.run(match_code))
        if not neighbors.empty:
            for i in range(neighbors.shape[0]):
                child_attribute = {}
                root_node_name = node_name[0:2]
                for key in neighbors[0][i]:
                    child_attribute[key] = neighbors[0][i][key]
                child_categary = '误码率: %s' % (str(round(neighbors[1][i]['error_rate'], 4)))
                children.append(make_child_json(root_node_name, child_attribute, child_categary))
    elif node_name[0:2] == '干扰':
        # 干扰与信号
        match_code = "MATCH(a {name:'%s'}) - [b:误码率] - (c) Return c,b ORDER BY b.error_rate DESC LIMIT %d" % \
                     (node_name, NEIGHBOR_NUM)
        neighbors = pd.DataFrame(G.run(match_code))
        if not neighbors.empty:
            for i in range(neighbors.shape[0]):
                child_attribute = {}
                root_node_name = node_name[0:2]
                for key in neighbors[0][i]:
                    child_attribute[key] = neighbors[0][i][key]
                child_categary = '误码率: %s' % (str(round(neighbors[1][i]['error_rate'], 4)))
                children.append(make_child_json(root_node_name, child_attribute, child_categary))
        # 干扰与干扰
        match_code = "MATCH(a) - [b:干扰相似] - (c {name:'%s'}) Return a,b ORDER BY b.Interference_similarity_ratio DESC LIMIT %d" % \
                     (node_name, NEIGHBOR_NUM)
        neighbors = pd.DataFrame(G.run(match_code))
        if not neighbors.empty:
            for i in range(neighbors.shape[0]):
                child_attribute = {}
                root_node_name = node_name[0:2]
                for key in neighbors[0][i]:
                    child_attribute[key] = neighbors[0][i][key]
                child_categary = '干扰相似度: %s' % (str(round(neighbors[1][i]['Interference_similarity_ratio'], 4)))
                children.append(make_child_json(root_node_name, child_attribute, child_categary))
    return children


def make_json(node_name):
    # 制作根节点属性
    root = make_root(node_name)
    # 制作邻居节点属性
    root['children'] = make_child(node_name)
    return root


app = Flask(__name__)
CORS(app, resource=r'/*')


@app.route('/')
def hello_world():
    return 'Hello World!'


# ###获得推理信号的数据，并调用creat.py中的推理
# @app.route('/add', methods=['POST'])
# def add_node():
#     setData = request.get_data(as_text=True)
#     setData = json.loads(setData)
#
#     ###先创建推理的信号节点
#     creat_node(setData)
#     time.sleep(10)
#     #判断信号输入的名字是否有重合
#     js1 = './2.json'
#     with open(js1) as f:
#         b = json.load(f)
#         print(b)
#         if b ==1:
#             ###创建信号相似相似度和误码率
#             get_newdata(setData)
#             return "0"
#         else:
#             return "请重新输入"


###获得推理信号的数据，并调用creat.py中的推理
@app.route('/add', methods=['POST'])
def add_node():
    setData = request.get_data(as_text=True)
    setData = json.loads(setData)
    t = threading.Thread(target=creat_node, args=(setData,))
    t1 = threading.Thread(target=get_newdata, args=(setData,))

    ###先创建推理的信号节点
    # proc.communicate()
    # creat_node(setData)
    t.start()
    time.sleep(10)
    #判断信号输入的名字是否有重合
    js1 = './2.json'
    with open(js1) as f:
        b = json.load(f)
        print(b)
        if b ==1:
            t.join()
            ###创建信号相似相似度和误码率
            # proc1.communicate()
            t1.start()
            # get_newdata(setData)
            time.sleep(10)
            t1.join()
            return "0"

        else:
            return "请重新输入"


#分别进行推理部分的信号节点查询和关系查询,当2.json中数字为1时，节点创建成功；2时，信号相似度关系创建成功；3时信号与干扰之间误码率关系创建成功
@app.route('/check', methods=['GET'])
def check():
    js1 = './2.json'
    with open(js1) as f:
        b = json.load(f)
    print(b)
    if b==1:
        print("节点创建成功")
        return "1"
    elif  b==2:
        print("信号相似度关系创建成功")
        return "2"
    elif  b==3:
        print("信号误码率创建成功")
        return "3"

#
#
# @app.route('/ch', methods=['GET'])
# def ch():
#     js1 = './2.json'
#     with open(js1) as f:
#         b = json.load(f)
#     print(b)
#     if b==2:
#         print("信号相似度关系创建成功")
#         return "2"
#
#
# @app.route('/th', methods=['GET'])
# def th():
#     js1 = './2.json'
#     with open(js1) as f:
#         b = json.load(f)
#     print(b)
#     if b==3:
#         print("误码率创建成功")
#         return "3"

# 初始化标签
@app.route('/init')
def init_label():
    ###2.json写进0，
    js='./2.json'
    a = 0
    with open(js, "w") as f:
        json.dump(a, f)
        print("推理已经准备好")
    signal_node = pd.DataFrame(G.run("MATCH(a:信号) return a['name'], a['Modulation_method']"))
    return_json = {
        'signalName': signal_node[0].tolist(),
        'signalColor': [{'label': '信号(%s)' % (label), 'color': NODE_COLOR[label]}
                        for label in set(signal_node[1].tolist())]
    }
    return jsonify(return_json)


# 获取节点类别
@app.route('/node_label', methods=['GET'])
def get_name():
    node_label = request.args.get('label')
    df = pd.DataFrame(node_matcher.match("信号", Modulation_method=node_label[3:-1]))
    result_name = df['name'].tolist()
    return jsonify(result_name)


# 获取节点邻居节点
@app.route('/child', methods=['GET'])
def get_child():
    node_name = request.args.get('name')
    # 以接收的节点作为根节点
    return_json = make_json(node_name)
    print(return_json)
    # print(return_json)

    return jsonify(return_json)


if __name__ == '__main__':

    # 开启后端
    app.run(debug=True, host='0.0.0.0', port=5000)

