# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import numpy as np
from multiprocessing import Pool 
import matplotlib.pyplot as plt


def mkdirectory(path):     
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
           
    
def save_results(resultpath_status,simulate_num,dic_status):
    fd = open(resultpath_status + 'sim'+str(simulate_num) + '_status.txt','w') 
    for n in dic_status:
        fd.write(str(n) + '\t'+ str(dic_status[n][0]) + '\t'+ str(dic_status[n][1]) +'\n')
    fd.close()
       

def Deal_R(args):  # 对于特定参数的网络——[Network ID,平均度,zeta,初始active的比例,阈值,模拟次数,存结果的路径,存处理结果的路径(2个)]
    i, avg_k, zeta, source_p,T_active,sim_time,resultpath_status,deal_results_time,deal_results_spatial = args
    print('Deal_R for netId:%d, source_p:%f' % (i, source_p))  
    f1 = open(deal_results_time +'active_result.txt','w', encoding='utf-8-sig')
    f2 = open(deal_results_time +'active_result_total.txt','w', encoding='utf-8-sig')
    for simulate_num in range(sim_time):  # 模拟总次数
        f1.write(str(simulate_num) + '\t')  # 写入模拟次数
        f2.write(str(simulate_num) + '\t')
        sum1 = 0  # 用于记录每次模拟的active总数
        dic_1 = {}   # 记录每次模拟每时步新增的active节点 key为时步,value为该时步inactive → active的节点坐标的列表
        f = open(resultpath_status +'sim'+str(simulate_num) + '_status.txt', 'r', encoding='utf-8-sig') 
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
                # 去除字符串的括号
                item = item.strip('()')
                # 分割字符串并转换为整数
                num1, num2 = map(int, item.split(','))
                new_list.append((num1, num2))
            sorted_dic1[key] = new_list
        
     
        if len(sorted_dic1) != 0:
        
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
       
    f1.close()
    f2.close()
    
         
    
    

def Deal_Parallel(i, zeta, avg_k, source_pro,T_active,sim_time):  # Network ID,zeta,平均度,初始active的比例,阈值,模拟次数
    args = []  # 按初始active的比例的列表的顺序，存[[Network ID,平均度,zeta,初始active的比例[0],阈值,模拟次数,最大迭代次数,存结果的路径,存处理结果的路径(2个)],[同前,仅初始active的比例变]]
    resultpath = 'result/'  # 存放模拟结果的文件夹
    deal_resultpath = 'deal_result/'  # 存放处理结果的文件夹
    for source_p in source_pro:
        deal_results_time =  deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/time_result/' # 存放时间上处理结果的路径
        deal_results_spatial =  deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/spatial_result/' # 存放空间上处理结果的路径
        resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/'  # 存放结果的路径
        mkdirectory(deal_results_time)  # 创建存放时间上处理结果的文件夹
        mkdirectory(deal_results_spatial)  # 创建存放空间上处理结果的文件夹
        args.append([i, avg_k, zeta,source_p,T_active,sim_time,resultpath_status,deal_results_time,deal_results_spatial]) 
    
    pool = Pool(processes=int(len(source_pro)/5))   # 创建一个进程池, 进程数量根据zetas列表的长度除以 5 来确定   
    pool.map(Deal_R, args)  # 把args列表中的每个元素作为参数传递给Percolation函数
    # 将这些任务分配给进程池中的多个进程并行执行,在所有任务都完成并返回结果之前，pool.map方法不会返回，主程序也会停在这里等待.
    pool.close()   # 关闭进程池
    
       
if __name__ == "__main__":
    # 网络涉及到的参数      
    # zeta取值的列表:[3,4,5,...19,20,30,40,50,...,90,100,500,1000]
    zeta = 3
    avg_k = 5   # 平均度
    i = 0
    source_pro = [x / 100 for x in range(0, 41)]   # 初始激活节点的比例:[0.01, 0.02, 0.03, 0.04,... 0.98,0.99,1.0]
    
    T_active = 4  # 邻居中有>=2个处于active时,inactive → active
    sim_time = 20  # 模拟次数
    
    Deal_Parallel(i, zeta, avg_k,source_pro,T_active,sim_time)   # 并行模拟
    
    
    
    
