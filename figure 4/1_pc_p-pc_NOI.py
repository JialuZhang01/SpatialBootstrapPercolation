# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 20:55:16 2025

@author: Administor
"""


import os 
import pickle as pk 
import copy 
import time
import ast

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
    
    sorted_dic = dict(sorted(dic_1.items()))  
    if len(sorted_dic) != 0:
        max_step = max(sorted_dic.keys())  
    else:
        max_step = 0    
    
  
    return max_step



def find_pc(zeta,L_nodes_random,avg_k,T_active,G,i,sim_t,L_nodes,L,position_cal):
  
    print('Random-Percolation for zeta:%d, position:%d' % (zeta, position_cal))   
    
    Dic_status_original = {}  
    for node in G.nodes():  
        
        Dic_status_original[node] = ['inactive',-1]
 
    Dic_status = copy.deepcopy(Dic_status_original)  
    List_source = L_nodes_random[:position_cal] 
    List_active = [] 
    for source_positive in List_source:  
        Dic_status[source_positive] = ['active', 0]  
        List_active.append(source_positive)  
    
    Dic_status_random = percolation_course(G,List_active,Dic_status,T_active,max_steps,L_nodes) 
    random_p_NOI=Get_P_infinite(Dic_status_random)
    
            
    return random_p_NOI
    



def read_nodes_seq(sim_t):
    f_nodes = open(path_read_pinf+'sim_p_nodes.txt','r',encoding= 'utf-8-sig')
    list_n = []
    for line_nodes in f_nodes:
        line_nodes = line_nodes.strip().split('\t')
        if line_nodes[0] == 'sim'+str(sim_t):
            for nodes_i in line_nodes[1:]:
                node_i = ast.literal_eval(nodes_i)
                list_n.append(node_i)
    f_nodes.close()
    return list_n
                
def generate_p(base_value):
    intervals = [
        
        (0.0001, 0.0001, 10),
        (0.002, 0.001, 9),   
        (0.02, 0.01, 9)     
    ]
    
    
    result = []
    for start_offset, step, count in intervals:
        current = base_value + start_offset
        for _ in range(count):
            
            result.append(round(current, 10))
            current += step
    
    return result       

    
       
if __name__ == "__main__":
    networkpath = 'network/'   
    
    L = 2000  
    N = L * L  
    zeta = 2000
    avg_k = 10   
    i = 0  # NetID
    T_active = 6 
    sim_time = 100 
    with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
        G = pk.load(f) 
    L_nodes = []   
    for node in G.nodes():  
        L_nodes.append(node)   
    

    max_steps = 5000000   
    
    path_read_pinf = 'deal_result/zeta='+str(zeta)+'/NetID='+str(i)+'/'
    path_write_pinf = path_read_pinf+'/p-p_c/'
    mkdirectory(path_write_pinf) 
    
    f_open1=open(path_read_pinf+'sim_p_pnoi.txt','r',encoding='utf-8-sig')
    f_open2=open(path_read_pinf+'sim_p_pc.txt','r',encoding='utf-8-sig')
    dic_sim_pc = {}
    for line_pc in f_open2:
        line_pc = line_pc.strip().split('\t')
        dic_sim_pc[int(line_pc[0][3:])] = float(line_pc[1][1:])
    f_open2.close()
    dic_sim_p ={}
    for line_noi in f_open1:
        line_noi = line_noi.strip().split('\t')
        dic_sim_p[int(line_noi[0][3:])] ={}
        for i in line_noi[1:]:
            i = i.strip().split(',')
            dic_sim_p[int(line_noi[0][3:])][float(i[0])] = int(i[1])  
    f_open1.close()
    
    
    for sim_t in range(sim_time):  
        init_t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(sim_t, init_t)
        L_nodes_random = read_nodes_seq(sim_t) 
        if len(L_nodes_random) != N:
            print('read random nodes list:fail')
        
        
        f_write1=open(path_write_pinf+'sim_p_pnoi.txt','a+',encoding='utf-8-sig')
        
        print('zeta='+str(zeta)+', sim_t:'+str(sim_t))
        sim_pc = dic_sim_pc[sim_t]
        p1 = generate_p(sim_pc) 
        
        
        f_write1.write('sim'+str(sim_t)+'\t'+str(sim_pc)+','+str(dic_sim_p[sim_t][sim_pc])+'\t') 
        random_p_noi_l = {}
        for p1_cal in p1:
            if p1_cal in dic_sim_p[sim_t]:
                random_p_noi_l[p1_cal] = dic_sim_p[sim_t][p1_cal]
            else:
                position_cal = round(p1_cal * N)
                sim_p1_noi = find_pc(zeta,L_nodes_random,avg_k,T_active,G,i,sim_t,L_nodes,L,position_cal)
                
                random_p_noi_l[p1_cal] = sim_p1_noi 
        
        
        for random_pnoi in random_p_noi_l:
            
            f_write1.write(str(random_pnoi)+','+str(random_p_noi_l[random_pnoi])+ '\t')
            
        f_write1.write('\n')
 
        f_write1.close()
       
       
       
        
    
    
    


   
   
    
   
        
    
        
        
        
    
    
    
    
    
    
    

    
    
    
    