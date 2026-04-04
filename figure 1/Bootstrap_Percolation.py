# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import random
import numpy as np
import pickle as pk 
from multiprocessing import Pool 
import copy 


def mkdirectory(path):     # 若文件夹不存在，建立它
    if not os.path.exists(path):
        os.makedirs(path)
   
   
def percolation_course(g,list_active,dic_status,t_active,max_steps,l_nodes):
    for i_t in range(1,max_steps):   # 最大迭代次数
        add_active = []   # 存放每一时步需要加入到active列表的节点
        inactive_nodes = list(set(l_nodes)-set(list_active))
        for inactive_n in inactive_nodes: # 遍历inactive节点 
            t_calculate = 0  # 记录该节点的邻居中有几个处于active
            for m in g.neighbors(inactive_n):   # 遍历其邻居
                if dic_status[m][0] == 'active':  # 若处于active,则该节点的邻居中active节点数+1
                    t_calculate += 1
            if t_calculate >= t_active:  # 若该节点的邻居中active节点数超过设置的阈值
                add_active.append(inactive_n)
        for a in add_active:
            dic_status[a] = ['active',i_t]    # 更新其状态及时步
            list_active.append(a)
        if len(add_active) == 0:   # 如果这一时步没有节点的状态改变，说明以后也不会有节点inactive→active
            break
    
    return dic_status
    
def save_results(resultpath_status,simulate_num,dic_status):
    fd = open(resultpath_status + 'sim'+str(simulate_num) + '_status.txt','w') 
    for n in dic_status:
        fd.write(str(n) + '\t'+ str(dic_status[n][0]) + '\t'+ str(dic_status[n][1]) +'\n')
    fd.close()
    
   
def Percolation(args):
    G,i, avg_k, zeta,source_i,T_active,sim_time,max_steps,networkpath,resultpath_status,Selected_sets,L_nodes = args
    
    Dic_status_original = {}  # 初始化所有节点的状态
    for node in G.nodes():  # 对每一个节点，初始化状态为---'inactive',-1
        Dic_status_original[node] = ['inactive',-1]
    
    for simulation in range(sim_time):  # 模拟次数
        # print(simulation)
        Dic_status = copy.deepcopy(Dic_status_original)  # 每次模拟设置全部处于inactive
        List_source = Selected_sets[simulation][source_i] # 选取的源头列表
        List_active = []  # 存放active节点的列表
        for source_positive in List_source:  # 遍历初始源头节点
            Dic_status[source_positive] = ['active', 0]  # 设置源头的状态
            List_active.append(source_positive)  # 将源头加入active列表
        Dic_status = percolation_course(G,List_active,Dic_status,T_active,max_steps,L_nodes)  # 传播过程
        save_results(resultpath_status, simulation,Dic_status)  # 把模拟结果保存到.txt文件中
    return Dic_status


    

def BPParallel(G,networkpath, i, zeta, avg_k, source_pro,T_active,sim_time,max_steps,Selected_sets,L_nodes):  # 网络路径,Network ID,zeta的列表,平均度,初始active的比例,阈值,模拟次数,最大迭代次数
    args = []  # 按source_pro取值的列表的顺序，存[[Network ID,平均度,zeta,初始active的比例[0],阈值,模拟次数,最大迭代次数,网络路径,存结果的路径],[同前,仅初始active的比例变]]
    resultpath = 'result/'  # 存放模拟结果的文件夹
    for source_p in source_pro:
        print('Percolation for netId:%d, source_p:%f' % (i, source_p)) 
        source_i = source_pro.index(source_p) 
        resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/'  # 存放结果的路径
        mkdirectory(resultpath_status)  # 创建存放结果的文件夹
        args.append([G,i, avg_k, zeta,source_i,T_active,sim_time, max_steps,networkpath,resultpath_status,Selected_sets,L_nodes]) 
       
    
    pool = Pool(processes=int(len(source_pro)/1))   # 创建一个进程池, 进程数量根据zetas列表的长度除以 5 来确定   
    pool.map(Percolation, args)  # 把args列表中的每个元素作为参数传递给Percolation函数
    # 将这些任务分配给进程池中的多个进程并行执行,在所有任务都完成并返回结果之前，pool.map方法不会返回，主程序也会停在这里等待.
    pool.close()   # 关闭进程池
    
    
    
def Select_nodes(n,l_nodes,source_pro,sim_t):
    sim_selected = {}
    for sim_t1 in range(sim_t):
        node_counts = [max(0, int(p * n)) for p in source_pro]  # 计算每个比例对应的节点数量
        for i0 in range(1, len(node_counts)):   #确保节点数量严格递增
            if node_counts[i0] <= node_counts[i0-1]:
                node_counts[i0] = node_counts[i0-1] + 1
                
        selected_sets = []
        previous_nodes = set()
                
        for count in node_counts:
            nodes_to_add = count - len(previous_nodes)  # 计算需要新增的节点数量
            if nodes_to_add > 0:   # 如果需要新增节点
                available_nodes = [a_n for a_n in l_nodes if a_n not in previous_nodes] # 从未选择的节点中随机选择
                new_nodes = random.sample(available_nodes, nodes_to_add)
                current_nodes = previous_nodes.union(new_nodes)
            else:
                current_nodes = previous_nodes.copy()
                
            selected_sets.append(current_nodes)  # 添加当前节点集合到结果列表
            previous_nodes = current_nodes  # 更新之前选择的节点
        sim_selected[sim_t1]=selected_sets

    
    return sim_selected
    
       
if __name__ == "__main__":
    print('begin')
    networkpath = 'network/'   # 网络文件夹
    # 网络涉及到的参数
    L = 1000  # 每行/列的节点数目L
    N = L * L  # 整个网络的总节点数N
    # zeta取值的列表:[3,4,5,...19,20,30,40,50,...,90,100,500,1000]
    zeta = 8
    avg_k = 10   # 设置平均度
    i = 0
    with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
        G = pk.load(f)  # 使用 pickle.load 方法从文件中反序列化对象
    L_nodes = []    # 网络的节点列表
    for node in G.nodes():  # 对每一个节点，初始化状态为---'inactive',-1
        L_nodes.append(node)   # 把节点加入节点列表 
    
    
    source_pro = [x / 1000 for x in range(85, 300)] # 初始激活节点的比例:[0.01, 0.02, 0.03, 0.04,... 0.98,0.99,1.0]
    
    T_active = 6  # 邻居中有>=2个处于active时,inactive → active
    sim_time = 10  # 模拟次数
    Selected_sets = Select_nodes(N,L_nodes,source_pro,sim_time)
    max_steps = 5000000   # 最大迭代次数
    BPParallel(G,networkpath, i, zeta, avg_k,source_pro,T_active,sim_time,max_steps,Selected_sets,L_nodes)   # 并行模拟
    
    
    

    
    
    
    
