from py2neo import Graph, Node, Relationship, RelationshipMatcher, NodeMatcher
import networkx as nx
import pandas as pd

# 连接图数据库
G = Graph("http://neo4jdata.lingbtech.com:7474/browser/", auth=('neo4j', 'ct012345678'))
node_matcher = NodeMatcher(G)
neighbor_matcher = RelationshipMatcher(G)
root_node = (pd.DataFrame(node_matcher.match(name='信号1'))).to_dict()
child_node = (pd.DataFrame(node_matcher.match(name='干扰935'))).to_dict()
print(root_node)
print(child_node)

print(pd.DataFrame(G.run("MATCH(a:信号) return a['name'], a['Modulation_method']")))
print(pd.DataFrame(node_matcher.match("信号", Modulation_method='16QAM'))['name'].tolist())
# df = pd.DataFrame(G.run("MATCH(a) - [b:信号相似] ->(c {name:'信号2'}) Return a,b, b['信号相似度']"))
# df = df.sort_values(by=2, ascending=False)
# print(df)
# for key in df[0][0]:
#     print(key, df[0][0][key])
# # print(df[0][0]['name'])
# print(df[1][0]['信号相似度'])

# match_code = "MATCH(a) - [b:误码率] ->(c {name:'%s'}) Return a,b ORDER BY b.误码率 DESC LIMIT %d" % ('信号1', 20)
# neighbors = pd.DataFrame(G.run(match_code))
# print(neighbors)
#print(neighbors.empty)
#print(neighbors)
#neighbors = neighbors.sort_values(by=2, ascending=False)
