from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import *
import json,time
import  re
import numpy as np




def creat_node(new_data):

    js='./2.json'
    a = 0
    with open(js, "w") as f:
        json.dump(a, f)
        print("推理开始")

    print(new_data)
    datapath = './demo1.csv'
    data = pd.read_csv(datapath)
    # graph = Graph("http://neo4jdata.lingbtech.com:7474/browser/", auth=("neo4j", "ct012345678"))
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "ct123456"))
    n1 = {"signal_way1": "16QAM", "signal_way2": "32QAM", "signal_way3": "64AM", }
    name = new_data['信号名称']
    Signal_bandwidth = new_data['信号带宽'] + "KHz"
    Carrier_frequency = new_data['载波频率'] + "MHz"
    Signal_power = new_data['信号功率'] + "dBm"
    Signal_to_noise_ratio = new_data['信噪比'] + "dB"

    ##检查数据库中是否有重名的信号的名字
    # js = './1.json'
    # a = 0
    # with open(js, "w") as f:
    #     json.dump(a, f)

    name2 = data["信号"]
    name2 = name2.drop_duplicates(keep='first', inplace=False)
    lr = []
    for group in name2:
        print(group)
        lr.append(group)
    print(lr)
    if name in lr:
        print(123)
        print("请重新输入")

    else:
        # ###将1写进csv中
        # js='./1.json'
        # a = 1
        # with open(js, "w") as f:
        #     json.dump(a, f)
        #     print("加载入文件完成...")

        print(new_data['调制方式'])
        Modulation_method = n1[new_data['调制方式']]
        print(Modulation_method)
        node1 = Node("信号",
                     name=name,
                     Signal_bandwidth=Signal_bandwidth,
                     Carrier_frequency=Carrier_frequency,
                     Signal_power=Signal_power,
                     Signal_to_noise_ratio=Signal_to_noise_ratio,
                     Modulation_method=Modulation_method
                     )
        #####################创建新节点
        graph.create(node1)

        a = 1
        js = './2.json'
        with open(js, 'w') as f:
            json.dump(a, f)
        print(a)
        print("11")

###
# def creat_similar(new_data):



def get_newdata(new_data):
    print(new_data)
    datapath = './demo1.csv'
    data = pd.read_csv(datapath)
    # graph = Graph("http://neo4jdata.lingbtech.com:7474/browser/", auth=("neo4j", "ct012345678"))
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "ct123456"))
    n1 = {"signal_way1": "16QAM","signal_way2": "32QAM", "signal_way3": "64AM",}
    name=new_data['信号名称']
    Signal_bandwidth = new_data['信号带宽']+ "KHz"
    Carrier_frequency = new_data['载波频率']+ "MHz"
    Signal_power = new_data['信号功率']+ "dBm"
    Signal_to_noise_ratio = new_data['信噪比']+ "dB"


    print(new_data['调制方式'])
    Modulation_method=n1[new_data['调制方式']]
    print(Modulation_method)
    node1 = Node("信号",
                 name=name,
                 Signal_bandwidth=Signal_bandwidth,
                 Carrier_frequency=Carrier_frequency,
                 Signal_power=Signal_power,
                 Signal_to_noise_ratio=Signal_to_noise_ratio,
                 Modulation_method=Modulation_method
                 )
    #####################创建新节点




    # print("创建成功")
    node_ls = []
    same = []
    # 找出完全一样的节点
    for i in range(data.shape[0]):
        # print(data.shape[0])
        # signal_bandwidth = str(data.iloc[i, :]['信号带宽'])+"KHz"
        # Carrier_frequency = str(data.iloc[i, :]['载波频率'])+"MHz"
        # Signal_power=str(data.iloc[i, :]['信号功率'])+"dBm"
        # Signal_to_noise_ratio=str(data.iloc[i, :]['信噪比'])+"dB"
        # name = data.iloc[i, :]['信号id']
        # Modulation_method=str(data.iloc[i, :]['调制方式'])

        Signal_bandwidth = node1['Signal_bandwidth']
        Carrier_frequency = node1['Carrier_frequency']
        Signal_power = node1['Signal_power']
        Signal_to_noise_ratio = node1['Signal_to_noise_ratio']
        Modulation_method = node1['Modulation_method']
        matcher = NodeMatcher(graph)
        node2 = matcher.match("信号", Signal_bandwidth=Signal_bandwidth, Signal_power=Signal_power,
                              Signal_to_noise_ratio=Signal_to_noise_ratio, Carrier_frequency=Carrier_frequency,
                              Modulation_method='16QAM', ).first()
        if node2 != None and node2['name'] != node1['name']:
            node_ls.append(node2['name'])
            same.append(node_ls[0])
    node_ls = set(node_ls)
    node_ls = list(node_ls)
    print("完全相同")
    # print(node_ls[0])

    ##获得完全相同的信号的干扰信号

    node_lr = []
    f1 = []
    # 找出信号相似得节点
    for i in range(data.shape[0]):
        # print(data.shape[0])
        Signal_bandwidth = node1['Signal_bandwidth']
        Carrier_frequency = node1['Carrier_frequency']
        Signal_power = node1['Signal_power']
        Signal_power1 = node1['Signal_power']
        # print(Signal_power1)
        Signal_power2 = re.findall(r'\d+\.*\d*', Signal_power1)
        # print(Signal_power2)
        Signal_power3 = float(Signal_power2[0])
        # print(Signal_power3)
        Signal_to_noise_ratio = node1['Signal_to_noise_ratio']
        Modulation_method = node1['Modulation_method']

        Signal_bandwidth1 = str(data.iloc[i, :]['信号带宽']) + "KHz"
        Carrier_frequency1 = str(data.iloc[i, :]['载波频率']) + "MHz"
        Signal_power0 = (data.iloc[i, :]['信号功率'])
        name = (data.iloc[i, :]['信号'])
        # print(Signal_power)
        # print(type(Signal_power))
        ##获得信号功率的数值

        # print(Signal_power3)
        # print(type(Signal_power3))

        Signal_to_noise_ratio1 = str(data.iloc[i, :]['信噪比']) + "dB"
        # Modulation_method = "16QAM"
        # Modulation_method=str(data.iloc[i, :]['调制方式'])
        # Modulation_method=node1['Modulation_method']
        matcher = NodeMatcher(graph)

        if (-0.5 < Signal_power0 - Signal_power3 < 0.5 and Signal_power0 - Signal_power3 != 0):

            node3 = matcher.match("信号", name=name, Signal_bandwidth=Signal_bandwidth,
                                  Signal_to_noise_ratio=Signal_to_noise_ratio, Carrier_frequency=Carrier_frequency,
                                  Modulation_method='16QAM').first()

            if node3 != None and node3['name'] not in node_lr:
                g1 = 1 - abs(Signal_power3 - Signal_power0) / Signal_power0
                print(g1)
                f1.append(g1)
                print(node3)
                node_lr.append(node3['name'])
                print(node_lr)
    print("相似的找到了")
    ##创建相似信号之间的关系
    for i in range(len(node_lr)):
        matcher = NodeMatcher(graph)
        name = node1['name']
        signal_node = matcher.match(name=name).first()
        # print(signal_node)
        signal_node1 = matcher.match(name=node_lr[i]).first()

        ber = f1[i]

        relationship = Relationship(signal_node, '信号相似', signal_node1, Signal_similarity_ratio=ber)
    ######################################################################(正式使用，下面创建关系注释掉)
        graph.create(relationship)

    a = 2
    js = './2.json'
    with open(js, 'w') as f:
        json.dump(a, f)
    print(a)
    print("12")
    time.sleep(15)


    ##相似信号的名字放在node_lr中

    # print(node_lr)
    print("相似的")
    data = pd.read_csv(datapath)
    ##找到相似信号的所有信息
    group_ls = []
    for i in range(0, len(node_lr)):
        Signal_power1 = node1['Signal_power']
        # print(Signal_power1)
        Signal_power2 = re.findall(r'\d+\.*\d*', Signal_power1)
        # print(Signal_power2)
        Signal_power3 = float(Signal_power2[0])
        name = node_lr[i]
        ##df是相似信号的所有信息
        df = data.loc[data["信号"] == name]
        group_ls.append(df)
        # print(df)
    ##将相似信号信息进行合并
    result = pd.concat(group_ls)
    # print(result)
    result1 = result.groupby(['干扰'])
    print(result)
    # result= result.groupby(['干扰']).filter(lambda x: len(x) >= 2)
    # print(result1)
    datapath = './demo.csv'
    data = pd.read_csv(datapath)
    for name, group in result1:

        ########若新信号完全相同，跳出for循环
        print(len(node_ls))
        if len(node_ls) != 0:
            break

        # print(group)
        # print(name)
        # print(group)
        # 读取节点1的信号功率
        Signal_power = node1['Signal_power']
        Signal_power1 = node1['Signal_power']
        # print(Signal_power1)
        Signal_power2 = re.findall(r'\d+\.*\d*', Signal_power1)
        # print(Signal_power2)
        Signal_power3 = float(Signal_power2[0])

        print(group)
        ##获得信号与干扰之间的误码率，放在d1中保存
        d1 = 0

        print(123)
        # f1=max(group.size())
        # print(f1)
        for i in range(len(group)):
            Signal_power7 = group.iloc[i, :]['信号功率']
            error_rate = group.iloc[i, :]['误码率']
            c1 = 1 - abs((Signal_power3 - Signal_power7) / Signal_power3)
            # print(len(node_lr))
            d1 += (c1 * error_rate) * 1 / len(node_lr)

        d1 = float(d1)
        print(d1)
        error_rate = group.iloc[0]['误码率']
        # print(error_rate)
        # print(len(node_lr))
        # print(len(group))
        if (len(node_lr) <= len(group) + 1 and -0.05 < d1 - error_rate < 0.05):
            ##新建信号与干扰之间的误码率为d1,干扰为name,可以在这里创建新建信号与干扰之间的关系
            matcher = NodeMatcher(graph)
            name1 = node1['name']
            # print(name)
            # print(name1)
            print(321)
            signal_node = matcher.match(name=name1).first()
            # print(signal_node)
            signal_node1 = matcher.match(name=name).first()
            relationship = Relationship(signal_node, '误码率', signal_node1, error_rate=d1)
            ####################################################创建新信号与干扰之间的关系
            graph.create(relationship)
            ##创建新信号与干扰之间的数据，准备写进csv文件中

            name1 = node1['name']
            # print(name1)
            Modulation_method = group.iloc[0]['调制方式']
            Signal_bandwidth = group.iloc[0]['信号带宽']
            Carrier_frequency = group.iloc[0]['载波频率']
            Signal_power = node1['Signal_power']

            Signal_power1 = node1['Signal_power']
            # print(Signal_power1)
            Signal_power2 = re.findall(r'\d+\.*\d*', Signal_power1)
            # print(Signal_power2)
            Signal_power3 = float(Signal_power2[0])
            Signal_to_noise_ratio = group.iloc[0]['信噪比']
            Interference_method = group.iloc[0]['干扰方式']
            Interference_bandwidth = group.iloc[0]['干扰带宽']
            Interference_frequency = group.iloc[0]['干扰频率']
            Interference_power = group.iloc[0]['干扰功率']
            s = pd.Series({"信号": name1, "调制方式": Modulation_method, "信号带宽": Signal_bandwidth, "载波频率": Carrier_frequency,
                           "信号功率": Signal_power3, "信噪比": Signal_to_noise_ratio,
                           "干扰": name, "干扰方式": Modulation_method, "干扰带宽": Interference_bandwidth,
                           "干扰频率": Interference_frequency, "干扰功率": Interference_power, "误码率": d1})
            # print(s)
            data = data.append(s, ignore_index=True)
            print(data)
            ######################将新信号的数据
            # data.to_csv('2.csv', header=True, index=None, encoding='utf_8_sig')

    a = 3
    js = './2.json'
    with open(js, 'w') as f:
        json.dump(a, f)
    print(a)
    print("13")
