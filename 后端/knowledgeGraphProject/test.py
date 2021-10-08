import pandas as pd
import json
from flask import Flask, request, jsonify
from flask_cors import *
import json


app=Flask(__name__)



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



if __name__ == '__main__':

    # 开启后端
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)



# ###将数据写进json文件中
# a=2
# js = './2.json'
# with open(js,'w') as f:
#     json.dump(a,f)
# print(a)