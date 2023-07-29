import pickle

with open('input.pickle', 'rb') as handle:
    b = pickle.load(handle)
sn_graph=b.get("substrate")
vn_graph=b.get("vne_list")  
sn_graph_BW=sn_graph.edge_weights
sn_cap={}

for i in range(sn_graph.nodes):
    sn_cap[i]=sn_graph.node_weights.get(i)
print("Initial CRB capacity of Substrate Network :\n",sn_cap,"\n")       
print("Initial BW capacity of Substrate Network :\n",sn_graph_BW,"\n") 

def nodeMap(vne,i,sn_status):
    for j in range(sn_graph.nodes):
        if(sn_status[j]<0):
            if(sn_cap.get(j)>=vne.node_weights.get(i)):
                sn_status[j]=0
                #sn_cap[j]-=vne.node_weights.get(i)
                return j
    return -1

def nodeMapUpd(Nodemapping,vne):
    for j in range(len(Nodemapping)):
        sn_cap[int(Nodemapping[str(j)])]-=vne.node_weights.get(j)
           
def edgeMap(u,v,allpath,vne):
    demand_uv=vne.edge_weights[(u, v)]
    i=0
    flag=0
    while(i<len(allpath)-1):
        u1=allpath[i]
        v1=allpath[i+1]
        if(sn_graph_BW[(u1,v1)]>=demand_uv):
            i+=1
            flag=1
        else:    
            flag=0
            break
    if(flag):
        i=0
        while(i<len(allpath)-1):
            u1=allpath[i]
            v1=allpath[i+1]
            sn_graph_BW[(u1,v1)]-=demand_uv
            i+=1  
    return flag

count=0

for i in range(len(vn_graph)):
    rev=0
    cost=0
    print("VNR",i+1,"\n")
    sn_status={}
    for k in range(sn_graph.nodes):
        sn_status[k]=-1    
    vne = vn_graph[i]
    # print("test----",vne.edges)
    print("Initial SN status :\n",sn_status)

    # Node Mapping
    Nodemapping = {}
    for j in range(vne.nodes):
        temp=nodeMap(vne,j,sn_status)
        if(temp>-1):
            Nodemapping[str(j)]=str(temp)
            rev+=vne.node_weights[j]
            cost+=vne.node_weights[j]
        # print("--------",j)
    print("SN status after node mapping :\n",sn_status)
    if(len(Nodemapping))==vne.nodes:
        print("Node mapping completed for VNR",i+1)
        print(Nodemapping,"\n")  
    else:
        print("Failed to embed all nodes of VNR", i+1, "--> VNR",i+1,"unsuccessful\n------------------------------------------")
        continue    
#     print(sn_status)    
#      print("Substrate Network CRB capacity after node mapping : ",sn_cap)
    # Link Mapping
    Linkmapping = {}
    for u,v in vne.edges:
        map_u = Nodemapping[u]
        map_v = Nodemapping[v]
        demand_uv = vne.edge_weights[(u, v)]
        rev+=demand_uv
        all_path_uv = sn_graph.printAllPaths(map_u, map_v, demand_uv)
        print("For Link:",u,"->",v,"All Path ",map_u,"->",map_v,":",all_path_uv)
        all_path_uv.sort(key = len)
        print("Sorted :",all_path_uv)
        print("\n")
        # print(len(all_path_uv))
        if len(all_path_uv) == 0:
            break
        else:
            for l in range(len(all_path_uv)):
                temp=edgeMap(u,v,all_path_uv[l],vne)
                if(temp):
                    Linkmapping[(u, v)] = all_path_uv[l]
                    cost+=(demand_uv)*(len(all_path_uv[l])-1)
                    break
                else:
                    continue
    
    if len(Linkmapping) == len(vne.edges):
        nodeMapUpd(Nodemapping,vne)
        print("Link mapping completed for VNR", i+1)
        print(Linkmapping,"\n")
        print("Embedding successful for VNR",i+1,"\n")
        count+=1
        print("Revenue/Cost Ratio for VNR",i+1,": ",(rev/cost)*100,"%\n------------------------------------------")  
    else:
        print("Failed to embed all links of VNR", i+1, "--> VNR",i+1,"unsuccessful\n------------------------------------------")
      
print("Acceptance ratio :",(count/len(vn_graph))*100,"%")
print("\nCRB capacity of Substrate Network after embedding:\n",sn_cap,"\n")
print("\nBW capacity of Substrate Network after embedding:\n",sn_graph_BW,"\n")
