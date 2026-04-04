# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import random
import numpy as np
import pickle as pk 
import copy 
import matplotlib.pyplot as plt
import ast
import networkx as nx



def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path,exist_ok=True)
        

def save(ResultPath, results): 
    """
    Serializes and saves simulation data to a binary file using pickle.

    Parameters:
        result_path (str): The destination file path (typically ends in .pkl or .bin).
        results (object): The Python object to be serialized.
    """
   pk.dump(results, open(ResultPath, "wb"))
   

def percolation_course(g,list_active,dic_status,t_active,max_steps,l_nodes): 
    """
    Execute the iterative bootstrap percolation process on a graph.
    
    Parameters:
        g (networkx.Graph): The underlying network.
        list_active (list): List of currently active nodes.
        dic_status (dict): Dictionary mapping nodes to their status ['active'/'inactive', time_step].
        t_active (int): Activation threshold (T).
        max_steps (int): Maximum number of iterations (time steps) allowed.
        l_nodes (list): List of all nodes.
        
    Returns:
        dict: Updated dic_status containing the final activation state and the time each node flipped.
    """
    for i_step in range(1,max_steps):  
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
            dic_status[a] = ['active',i_step]    
            list_active.append(a)
        if len(add_active) == 0:   
            break
    
    return dic_status
    

def save_results(resultpath_status,simulate_num,dic_status):
   """
    Exports the status and activation time of each node to a text file.
    
    Parameters:
        resultpath_status (str): Directory path where the results will be saved.
        simulate_num (int): The current simulation realization/index.
        dic_status (dict): Dictionary mapping nodes to [status, activation_time].
    """
    fd = open(resultpath_status + 'sim'+str(simulate_num) + '_status.txt','w') 
    for n in dic_status:
        fd.write(str(n) + '\t'+ str(dic_status[n][0]) + '\t'+ str(dic_status[n][1]) +'\n')
    fd.close()
    


def Percolation(G,i, avg_k, zeta,source_i,T_active,sim_t, max_steps,networkpath,resultpath_status,Selected_sets,L_nodes):
    """
    Main driver function for bootstrap percolation simulations.
    
    Parameters:
            G (networkx.Graph): The spatial network.
            i, avg_k, zeta: Network parameters (index, average degree, link length).
            source_i: Index for the pre-selected initial seed set.
            T_active (int): Activation threshold (T).
            sim_t (int): An independent simulation realizations.
            max_steps (int): Maximum time steps for each cascade.
            networkpath, resultpath_status: IO paths for loading/saving.
            Selected_sets (list): Pre-generated initial seed nodes for all simulations.
            L_nodes (list): List of all nodes.

    """
    Dic_status_original = {} 
    for node in G.nodes(): 
        Dic_status_original[node] = ['inactive',-1]
    
    Dic_status = copy.deepcopy(Dic_status_original) 
    List_source = Selected_sets[sim_t][source_i]
    List_active = []  
    for source_positive in List_source: 
        Dic_status[source_positive] = ['active', 0]  
        List_active.append(source_positive)  
    Dic_status = percolation_course(G,List_active,Dic_status,T_active,max_steps,L_nodes)  
    save_results(resultpath_status, sim_t,Dic_status)  
    


def deal_results(i, zeta, avg_k,sim_r,T_active,sim_t):
    resultpath = 'result/'  # 存放模拟结果的文件夹
    deal_resultpath = 'deal_result/time_result/zeta='+str(zeta)+'/sim_time='+str(sim_t)+'/'  # 存放处理结果的文件夹
    deal_results_time =  deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/time_result/' # 存放时间上处理结果的路径
    resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/'  # 存放结果的路径
    mkdirectory(deal_results_time)  # 创建存放时间上处理结果的文件夹
    
    print('Deal_R for <k>:%f, source_r:%d' % (avg_k, sim_r)) 
    # f1记录对于该次模拟 此次模拟的active总数 0;节点1;节点2;...(0时步激活的节点) 1;节点1;节点2;...(1时步激活的节点) ...
    f1 = open(deal_results_time +'active_result.txt','w', encoding='utf-8-sig') 
    # f2记录对于该次模拟 节点1 节点2 ...(只写active节点)
    f2 = open(deal_results_time +'active_result_total.txt','w', encoding='utf-8-sig')
    
    f1.write(str(sim_t) + '\t')  # 写入模拟次数
    f2.write(str(sim_t) + '\t')  # 写入模拟次数
    sum1 = 0  # 用于记录每次模拟的active总数
    dic_1 = {}   # 记录每次模拟每时步新增的active节点 key为时步,value为该时步inactive → active的节点坐标的列表
    f = open(resultpath_status +'sim'+str(sim_t) + '_status.txt', 'r', encoding='utf-8-sig') 
    for line in f:   # 遍历每一个节点
        line = line.strip().split('\t')
        if line[1] == 'active':   # 如果节点的状态为active
            sum1 += 1  # 此次模拟的active总数+1
            if int(line[2]) not in dic_1:   # 若该时步没有节点inactive → active
                dic_1[int(line[2])] = []     # 初始化该时步inactive → active的节点坐标的列表为空
            dic_1[int(line[2])].append(line[0])   # 把inactive → active的节点坐标加入对应时步
    f1.write(str(sum1) + '\t')   # 写入此次模拟的active总数
    sorted_dic = dict(sorted(dic_1.items()))  # 对dic_1按时步从小到大排序
    sorted_dic1 = {}  # sorted_dic 中列表里的字符串形式的元组转换为实际的元组形式
    for key, value in sorted_dic.items():
        new_list = []
        for item in value:
            item = item.strip('()') # 去除字符串的括号
            num1, num2 = map(int, item.split(',')) # 分割字符串并转换为整数
            new_list.append((num1, num2))
        sorted_dic1[key] = new_list
   
    if len(sorted_dic1) != 0: # 如果此次模拟有active节点（初始p=0时最终没有active的）
        max_step = max(sorted_dic1.keys())  # 返回此次模拟最大的时步
    else:
        max_step = 0
    x_step =  np.arange(max_step+1) # 横轴：时步
    y_accumulate = [0  for a in range(max_step+1)]   # 记录当前时步累计的active节点数
    
    for step in sorted_dic1:  # 对每一时步
        f1.write(str(step) + ';')
        y_accumulate[step] += len(sorted_dic1[step])  # 加上当前时步新增的
        for z in range(len(sorted_dic1[step])):  # 对该时步下的inactive → active的节点列表
            f2.write(str(sorted_dic1[step][z]) +'\t')
            if z != len(sorted_dic1[step]) - 1:
                f1.write(str(sorted_dic1[step][z]) +';')
            else:
                f1.write(str(sorted_dic1[step][z]) +'\t')
    f1.write('\n')
    f2.write('\n')
    f.close()
    for active_new in range(1,len(y_accumulate)):  # 转成累计数
        y_accumulate[active_new] += y_accumulate[active_new-1] 
   
    f2.close()
            
    
# Network ID, zeta,<k>,r,阈值,某次模拟次数
def find_pfinal(i, zeta, avg_k,sim_r,T_active,sim_t):  # 计算序参量
    deal_resultpath = 'deal_result/time_result/zeta='+str(zeta)+'/sim_time='+str(sim_t)+'/'# 存放处理结果的文件夹
    networkpath = 'network/'   # 网络文件夹 
    with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
        G_initial = pk.load(f)  # 使用 pickle.load 方法从文件中反序列化对象
    dic_r_pfinal = {}  #存放该r对应的该次模拟结果的最终最大连通量的节点的比例  key: r,value:[该次模拟结果的p∞]
    print('z='+str(zeta)+', r:'+str(sim_r))
    dic_r_pfinal[sim_r]=[]
    # f记录对于该次模拟 节点1 节点2 ...(只写active节点)
    f = open(deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/time_result/active_result_total.txt','r',encoding ='utf-8-sig') 
    for line in f:
        G = copy.deepcopy(G_initial)  # 初始的网络
        list_active =[]   # 存放此次模拟的active节点
        line = line.strip().split('\t')
        for j in line[1:]:
            list_active.append(j)
        l_active = [ast.literal_eval(item) for item in list_active]
        G1 = nx.subgraph(G, l_active)
        components = list(nx.connected_components(G1))  # 计算剩余网络的连通量
        if len(components) == 0 :
            dic_r_pfinal[sim_r].append(0)
            p_final = 0
        else:
            largest_component = max(components, key=len)  # 计算剩余网络的最大连通量
            p_final = int(len(largest_component))/N
            dic_r_pfinal[sim_r].append(p_final)
    f.close()
    path0 = 'deal_result/LCC_text/zeta'+str(zeta)+'/sim_time='+str(sim_t)+'/' 
    mkdirectory(path0) 
    f_w = open(path0+'T='+str(T_active) +'_avgk='+str(avg_k) +'_max_connexted.txt','a+', encoding='utf-8-sig')
    for i0 in dic_r_pfinal: 
        f_w.write('zeta'+ str(zeta)+'\t'+'r'+str(i0) + '\t')
        for j in range(len(dic_r_pfinal[i0])):
           if j != len(dic_r_pfinal[i0]) -1:
               f_w.write(str(dic_r_pfinal[i0][j])+'\t')
           else:
               f_w.write(str(dic_r_pfinal[i0][j])+'\n')
    f_w.close()
        
    return p_final
    
 
# 半径大小,该<k>对应的原始网络,存网络的文件夹,Network ID,zeta,<k>,阈值,某次模拟次数,最大迭代次数,每次模拟每个r下对应的种子节点,网络的节点列表   
def BP_deal_pfinal(sim_r,G,networkpath, i, zeta, avg_k,T_active,sim_t,max_steps,Selected_sets,L_nodes): # 该r下该次模拟得到的p∞
    resultpath = 'result/'  # 存放模拟结果的文件夹
    print('Percolation for avg_k:%f, source_r:%d' % (avg_k, sim_r)) 
    resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/'  # 存放结果的路径
    source_i = radius_list.index(sim_r)  # 该r对应在 存取所有初始选取半径的列表中的索引
    mkdirectory(resultpath_status)  # 创建存放结果的文件夹
    Percolation(G,i, avg_k, zeta,source_i,T_active,sim_t, max_steps,networkpath,resultpath_status,Selected_sets,L_nodes)  # bootstrap渗流
    deal_results(i, zeta, avg_k,sim_r,T_active,sim_t)  # 处理结果
    p_infin = find_pfinal(i, zeta, avg_k,sim_r,T_active,sim_t)  # 计算序参量
    
    
    return p_infin
    

  
# 初始选取的半径大小的列表,该<k>对应的原始网络,存网络的文件夹,Network ID,zeta,<k>,阈值,总模拟次数,最大迭代次数,每次模拟每个r下对应的种子节点,网络的节点列表
def find_rc(radius_l,G,networkpath, i, zeta, avg_k,T_active,sim_time,max_steps,Selected_sets,L_nodes): # 找该<k>下sim_time次的rc
    k_rc_l = []  # 记录该<k>下sim_time次的rc
    for sim_t in range(sim_time):  # 遍历模拟次数
        left, right = 0, len(radius_l) - 1   # 初始左边索引是0，右边索引是L/2 -1 =249
        rc_index = -1  # 用于记录rc 在radius_l中的索引, 初始是-1
    
        while left <= right:  # 只要左边索引 ≤ 右边索引
            mid = (left + right) // 2  # 每次循环要计算的r 在radius_l中的索引
            # 传入该半径, 调用bootstrap渗流_处理结果_计算序参量
            p_infinite = BP_deal_pfinal(radius_l[mid],G,networkpath, i, zeta, avg_k,T_active,sim_t,max_steps,Selected_sets,L_nodes)  
    
            if p_infinite >= 0.9:  # 如果在该r下得到的序参量≥0.9
                rc_index = mid
                right = mid - 1  # 继续在左半部分查找
            else:   # 如果在该r下得到的序参量 < 0.9
                left = mid + 1  # 继续在右半部分查找
                
        # 如果rc 在radius_l中的索引值不是-1,就说明找到了一个有限的rc;
        # 如果rc 在radius_l中的索引值是-1,就返回rc= L/2 =250;
        k_rc_l.append(radius_l[rc_index])
        
    return k_rc_l
   

def points_in_circle(l_nodes, radius_list, l_size,sim_t):
    sim_selected = {}
    for sim_t1 in range(sim_t):
        index_n = random.randint(0,len(l_nodes)-1)
        center_node = l_nodes[index_n]
        x0, y0 = center_node
        point_sim = []
        for radius in radius_list:
            r2 = radius ** 2
            points = set()
            for x in range(l_size):
                for y in range(l_size):
                    dx = min(abs(x - x0), l_size - abs(x - x0))
                    dy = min(abs(y - y0), l_size - abs(y - y0))
                    if dx * dx + dy * dy <= r2:
                        points.add((x, y))
            point_sim.append(points)
        sim_selected[sim_t1]=point_sim
    return sim_selected

       
if __name__ == "__main__":
    networkpath = 'network/'   # 网络文件夹
    # 网络涉及到的参数
    L = 500  # 每行/列的节点数目L
    N = L * L  # 整个网络的总节点数N
    T_active = 6  # 邻居中有>=2个处于active时,inactive → active
    sim_time = 1  # 模拟次数
    
    zeta = 5  # 本程序只对一个zeta,计算不同<k>下的rc
    avg_k_list  = [a_k / 10 for a_k in range(100, 151)] # <k>列表：[10.0,15.0]
    i = 0
    max_r= 251  # 最大的局部挑选范围选为L/2=250
    
    path_write_rc = 'deal_result/avgk_rc/'
    mkdirectory(path_write_rc) 
    f_write=open(path_write_rc+'zeta='+str(zeta)+'_k_rc.txt','a+',encoding='utf-8-sig') # f_write记录对于该zeta,每个<k>下的rc
    
    for avg_k in avg_k_list:  # 遍历<k>
        f_write.write('<k>'+str(avg_k)+'\t')  # f_write每一行先写入<k>*
        print('zeta='+str(zeta)+', avg_k:'+str(avg_k))
        with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
            G = pk.load(f)  # 使用 pickle.load 方法从文件中反序列化对象
        L_nodes = []    # 网络的节点列表
        for node in G.nodes():  # 对每一个节点,把节点加入节点列表 
            L_nodes.append(node)  
        
        radius_list = [r_initial for r_initial in range(max_r)]  # 初始选取的半径的大小，包含在该范围内的所有节点作为种子
        
        # Selected_sets:key为模拟次数,value该次模拟为[{r=0选的种子},{r=1选的种子},{r=2选的种子},...]
        Selected_sets = points_in_circle(L_nodes, radius_list, L,sim_time)
        max_steps = 5000000   # 最大迭代次数
        
        # 找该<k>下sim_time次的rc, k_rc_list:[该<k>下第1次模拟的rc, 该<k>下第2次模拟的rc,...]
        k_rc_list=find_rc(radius_list,G,networkpath, i, zeta, avg_k,T_active,sim_time,max_steps,Selected_sets,L_nodes)  
    
        for rc in range(len(k_rc_list)):  # f_write每一行写入<k>* 后,写入每一次的rc
            if rc!= len(k_rc_list)-1:
                f_write.write(str(k_rc_list[rc])+ '\t')
            else:
                f_write.write(str(k_rc_list[rc])+ '\n')
    f_write.close()
               
           
        
        
       
    
    

    
    
    
    
