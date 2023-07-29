import pickle
import pprint

with open('input.pickle', 'rb') as handle:
    b = pickle.load(handle)

sn_graph=b.get("substrate")
nodes_sn_graph=sn_graph.nodes

SN_node_CRB=sn_graph.node_weights
SN_edge_BW=sn_graph.edge_weights

#sn_ecap=sn_graph.edge_weights

with open("OutputPickle.txt", "a") as f:
  pprint.pprint("Substrate NW Nodes : ",stream=f)
  pprint.pprint(nodes_sn_graph, stream=f)
  pprint.pprint("Substrate NW CRB Capacity : ",stream=f)
  pprint.pprint(SN_node_CRB, stream=f)
  pprint.pprint("Substrate BW Capacity : ",stream=f)
  pprint.pprint(SN_edge_BW, stream=f)
  #pprint.pprint(sn_ecap[('0','1')], stream=f)

vn_graph=b.get("vne_list")

for i in range(len(vn_graph)):
  VNR='VNR '+str(i+1)
  nodes_vn_graph_0=vn_graph[i].nodes
  VN_node_CRB=vn_graph[i].node_weights
  VN_node_BW=vn_graph[i].edge_weights
  with open("OutputPickle.txt", "a") as f:
    pprint.pprint(VNR,stream=f) 
    pprint.pprint("Nodes :",stream=f)  
    pprint.pprint(nodes_vn_graph_0, stream=f)
    pprint.pprint("CRB Demand :",stream=f) 
    pprint.pprint(VN_node_CRB, stream=f)
    pprint.pprint("BW Demand :",stream=f) 
    pprint.pprint(VN_node_BW, stream=f)


