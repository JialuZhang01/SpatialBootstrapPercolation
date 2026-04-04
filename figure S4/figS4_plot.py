# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 15:54:19 2025

@author: JialuZhang01
"""
import os 
import numpy as np
import math
import networkx as nx
import pickle as pk
import math
import ast
import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    L = 1000  # 每行/列的节点数目L
    N = L * L  # 整个网络的总节点数N
    

    sim_time = 1  # 模拟次数
    
    zeta_l = [20,30,15,12,10] # The list of zeta values
    c_list =['#1072BD','#7F318D','#EDB021','#D7592C','#77AE43']
    c_index=0
    plt.figure(figsize=(10, 5)) 
    for z in zeta_l: 
        f = open('deal_result_rg/T=6/zeta='+str(z)+'/t_radius.txt','r',encoding='utf-8-sig')
        t = []
        r = []
        for i in f:
            i = i.strip().split('\t')     
            t.append(int(i[0][1:]))
            r.append(math.sqrt(float(i[1])))   
        f.close()
        # plt.plot(t,r,ls='-', lw=2, color=c_list[c_index], alpha = 1,label='ζ'+str(z))
        # 画线+空心点（核心参数配置）
        plt.plot(
            t, r,
            ls='-',          # 线型：实线
            lw=1,            # 线宽：2
            color=c_list[c_index],  # 线颜色（与点边缘色一致）
            alpha=1,         # 透明度：不透明
            label=f'ζ={z}',   # 图例：ζ+参数值
            # 以下是点相关参数
            marker='o',      # 点样式：圆形（可选 's'正方形、'^'三角形等）
            markersize=8,    # 点大小：6（按需调整）
            markeredgecolor=c_list[c_index],  # 点边缘色：与线颜色一致
            markerfacecolor='none',           # 点填充色：透明（空心效果）
            # markeredgewidth=1,                # 点边缘宽度：2（与线宽呼应，更协调）
        )
        c_index+=1
        
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.xlabel(r't', fontsize=24)
    plt.ylabel(r'$R_g$', fontsize=24)
    # plt.title('branching process', fontsize=21)
    plt.legend(frameon=False,fontsize=18,ncol=1)
    plt.savefig('deal_result_rg变化/fig4c_补充.pdf')
    plt.tight_layout()
    plt.show()

        
    
    
    
  
    
   
    
  
            


























        
        
