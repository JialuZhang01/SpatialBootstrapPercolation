# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 21:15:13 2025

@author: Administor
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: Administor
"""
import os
import random
import pickle as pk 
import copy 
import time
import networkx as nx


def mkdirectory(path):     
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        

def save(ResultPath, results):  
   pk.dump(results, open(ResultPath, "wb"))
   
   
def percolation_course(g,list_active,dic_status,t_active,max_steps,l_nodes):
    for i_t in range(1,max_steps):  
        add_active = []   
        inactive_nodes = list(set(l_nodes)-set(list_active)) 
        for inactive_n in inactive_nodes:  
            t_calculate = 0  
            for m in g.neighbors(inactive_n):  
                if dic_status[m][0] == 'active':  
                    t_calculate += 1
            if t_calculate >= t_active:  
                add_active.append(inactive_n)
        for a in add_active:
            dic_status[a] = ['active',i_t]
            list_active.append(a)
        if len(add_active) == 0:  
            break
    
    return dic_status

        
def Get_P_infinite(dic_status_cal):
    list_active_cal =[]   
    dic_1 = {}   
    for i_cal in dic_status_cal:
        if dic_status_cal[i_cal][0] == 'active':
            list_active_cal.append(i_cal)
            if int(dic_status_cal[i_cal][1]) not in dic_1:   
                dic_1[int(dic_status_cal[i_cal][1])] = []    
            dic_1[int(dic_status_cal[i_cal][1])].append(dic_status_cal[i_cal][0])   
    
    G1 = nx.subgraph(G, list_active_cal)  
    connected_components = sorted(nx.connected_components(G1), key=len, reverse=True)  
    if len(connected_components) == 0 :
        p_inf = 0
    else:
        largest_component = connected_components[0]  
        p_inf = int(len(largest_component))/(L**2)
  
    sorted_dic = dict(sorted(dic_1.items()))  
    if len(sorted_dic) != 0:
    
        max_step = max(sorted_dic.keys()) 
    else:
        max_step = 0           
    return p_inf,max_step
    

def find_pc(zeta,L_nodes_random,avg_k,T_active,G,i,sim_t,L_nodes,L,mid):
    print('Random-Percolation for zeta:%d, position:%d' % (zeta, mid))   # bootstrap  
    Dic_status_original = {}  
    for node in G.nodes():  
        Dic_status_original[node] = ['inactive',-1]
    


    Dic_status = copy.deepcopy(Dic_status_original)  
    List_source = L_nodes_random[:mid] 
    List_active = []  
    for source_positive in List_source: 
        Dic_status[source_positive] = ['active', 0] 
        List_active.append(source_positive)  
    Dic_status_random = percolation_course(G,List_active,Dic_status,T_active,max_steps,L_nodes)  
    random_p_infinite,random_p_NOI=Get_P_infinite(Dic_status_random)
    
    
    
    
       
            
    return random_p_infinite,random_p_NOI
    

def find_critical_p(zeta,L_nodes_random,avg_k,T_active,G,i,sim_t,L_nodes,L):
    n = len(L_nodes_random)
    max_possible = n // 3  
    # low=1，high=max_possible
    low = 1
    high = max_possible
    critical_k = 0  
    random_p_infinite_list = {} 
    random_p_noi = {}
    
    
    while low <= high:
        mid = (low + high) // 2  
        
       
        random_p_inf,random_p_n = find_pc(zeta,L_nodes_random,avg_k,T_active,G,i,sim_t,L_nodes,L,mid)
        source_p=mid/(L**2)
        random_p_infinite_list[source_p]=random_p_inf
        random_p_noi[source_p]=random_p_n
        
        if random_p_inf>0.9:
            
            critical_k = mid  
            high = mid - 1
        else:
            
            low = mid + 1
    return critical_k,random_p_infinite_list,random_p_noi 
    
  


    
       
if __name__ == "__main__":
    networkpath = 'network/'   
   
    L = 2000 
    N = L * L 
    zeta = 2000
    avg_k = 10   
    i = 0  
    T_active = 6 
    sim_time = 100  
    with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
        G = pk.load(f)  #pickle.load 
    L_nodes = []    
    for node in G.nodes():  
        L_nodes.append(node)   
    

    max_steps = 5000000   
    
    path_write_pinf = 'deal_result/zeta='+str(zeta)+'/NetID='+str(i)+'/'
    mkdirectory(path_write_pinf) 
 
    for sim_t in range(sim_time):  
        init_t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(sim_t, init_t)
        L_nodes_random = random.sample(L_nodes, k=len(L_nodes))  
        
        f_write=open(path_write_pinf+'sim_p_pinf.txt','a+',encoding='utf-8-sig')
        f_write1=open(path_write_pinf+'sim_p_pnoi.txt','a+',encoding='utf-8-sig')
        f_write2=open(path_write_pinf+'sim_p_pc.txt','a+',encoding='utf-8-sig')
        f_write3=open(path_write_pinf+'sim_p_nodes.txt','a+',encoding='utf-8-sig')
        f_write3.write('sim'+str(sim_t)+'\t') 
        for nodes0 in L_nodes_random:
            f_write3.write(str(nodes0)+'\t')
        f_write3.write('\n')
        f_write.write('sim'+str(sim_t)+'\t') 
        f_write1.write('sim'+str(sim_t)+'\t') 
        f_write2.write('sim'+str(sim_t)+'\t') 
        print('zeta='+str(zeta)+', sim_t:'+str(sim_t))
        critical_p,random_p_infinite_l,random_p_noi_l = find_critical_p(zeta,L_nodes_random,avg_k,T_active,G,i,sim_t,L_nodes,L)
        f_write2.write('p'+str(critical_p/(L**2))+'\n') 
        for random_pinf in random_p_infinite_l:  
            f_write.write(str(random_pinf)+','+str(random_p_infinite_l[random_pinf])+ '\t')
        f_write.write('\n')
        
        for random_pnoi in random_p_noi_l:
            f_write1.write(str(random_pnoi)+','+str(random_p_noi_l[random_pnoi])+ '\t')  
        f_write1.write('\n')
        f_write.close()
        f_write1.close()
        f_write2.close()
        f_write3.close()
       
        
    
    
    


   
   
    
   
        
    
        
        
        
    
    
    
    
    
    
    

    
    
    
    