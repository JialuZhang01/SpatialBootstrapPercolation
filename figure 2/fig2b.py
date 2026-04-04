# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: Administor
"""

import os
import numpy as np
import pickle as pk 
import matplotlib.pyplot as plt
import copy
import ast
import networkx as nx
from matplotlib.colors import ListedColormap


def mkdirectory(path):     # 若文件夹不存在，建立它
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
 
       
if __name__ == "__main__":
    # 网络涉及到的参数 
    L_side = 1000
    networkpath = 'network/'   # 网络文件夹   
    # zeta取值的列表:[3,4,5,...19,20,30,40,50,...,90,100,500,1000]
    zeta = 20  # 1000-243
    source_p = 0.236
    avg_k = 10   # 平均度
    i = 0
    T_active = 6  # 邻居中有>=2个处于active时,inactive → active 
    sim_time = 1
    deal_resultpath = 'deal_result/'
    deal_results_spatial =  deal_resultpath +'spatial_图2.d/'+ f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/spatial_result_total/'
    
  
    f1 = open('deal_result/3、12、1000级联过程txt结果/'+'T='+str(T_active) +'_avgk='+str(avg_k) +'_t_S(gc)_nodes_zeta'+str(zeta)+'_'+str(source_p)+'.txt','r', encoding='utf-8-sig')
    # 每一行：r* 节点1;节点2;..节点n(t0时位于最大连通分量中的节点); t1时位于最大连通分量中的节点 ...
    t = 0
    for line_f1 in f1:
        line_f1 = line_f1.strip().split('\t')
        if line_f1[0] == 'p'+str(source_p):
            for i in line_f1[1:]:  # i=[t0时位于最大连通分量中的节点,t1时位于最大连通分量中的节点,...]
                color_matrix = np.zeros((L_side, L_side))  # 最初每个节点的矩阵元素都是0
                lcc_nodes =[] # 当前时步最大连通分量中的节点集合
                if i != 'null':  # 若当前时步位于最大连通分量中的节点列表不为空
                    i = i.strip().split(';')  # t*时位于最大连通分量中的节点i=[节点1,节点2,...,;]
                    for n1 in i[0:-1]:   # 因为最后一个元素是分号
                        lcc_nodes.append(ast.literal_eval(n1))   
                for i0, j0 in lcc_nodes:  # 设置当前时步最大连通分量中的节点的矩阵元素为1
                    # color_matrix[int(i0-300)%L_side, int(j0+200)%L_side] = 1   # 12
                    color_matrix[int(i0), int(j0)] = 1
                    
                cmap = ListedColormap(['#885F9C', '#5BAB54'])  # 蓝色、绿色
                plt.imshow(color_matrix, cmap=cmap, origin='lower', vmin=0,vmax=1)
                plt.xticks([])
                plt.yticks([])
                plt.xlim(0, L_side)
                plt.ylim(0, L_side)
                plt.box(False)
                plt.title(f't={t}',fontsize=24)
                
                mkdirectory(deal_results_spatial+ str(0) + '_simulation/')  
                plt.savefig(deal_results_spatial+ str(0) + '_simulation/'+ 'step_'+ str(t)+'.pdf',bbox_inches = 'tight')
                # plt.savefig(deal_results_spatial+ str(0) + '_simulation/'+ 'step_'+ str(t)+'.png',bbox_inches = 'tight',dpi = 1000)
                plt.close()
                t+=1   
               
                print('t:'+str(t))
            break
    
    f1.close()
                

    
