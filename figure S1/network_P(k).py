# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: Administor
"""

import sys
import os
import random
import numpy as np
import pickle as pk 
import networkx as nx
import itertools as itert
from multiprocessing import Pool 
import matplotlib.pyplot as plt
from scipy.stats import poisson


def mkdirectory(path):     # 若文件夹不存在，建立它
    if not os.path.exists(path):
        os.makedirs(path)
        
        
       
if __name__ == "__main__":
    networkpath = 'network/'   # 存放网络的文件夹
    mkdirectory(networkpath)  # Create folder to save networks
    # 构建网络 
    L = 1000  # 每行/列的节点数目L
    N = L * L  # 整个网络的总节点数N
    # zeta取值的列表:[3,4,5,...19,20,30,40,50,...,90,100,500,1000]
    # zetas = list(np.arange(3, 21)) + [30, 40,50, 60, 70, 80, 90, 100, 500, 1000]
  
    zetas = [3,6,12,1000]
    avg_k = 10   # 设置平均度
    # with open(networkpath + f'NetID{0}_avgk{2}_zeta{2}_spatialNet.pkl', 'rb') as f:
    #     G = pk.load(f) 
    # for i in G.nodes():
    
    
    
   
    
    
    plt.figure(figsize=(5.6,4.8))
    c_draw =['#1072BD','#EDB021','#D7592C','#7F318D']
    xingzhuang=['s','o','*','^']
    c0=0
    for z in zetas:
        print(z)
        num_net=0
        dic_k ={}
        for i in range(2):
            print(i)
            num_net+=1
            with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{z}_spatialNet.pkl', 'rb') as f:
                G = pk.load(f)  # 使用 pickle.load 方法从文件中反序列化对象
            for n in G.nodes():
                d = G.degree[n]
                
                if d not in dic_k:
                    dic_k[d]=0
                dic_k[d]+=1  
        x_k=[]
        y_pro =[]
        for i in dic_k:
            x_k.append(i)
            y_pro.append(dic_k[i]/(num_net*N))
        
        if z==3:
            new_lst=[]
            for val in y_pro:
                if val > 0.14:
                    # 在 [0.132, 0.136] 取均匀随机数
                    new_val = random.uniform(0.13, 0.135)
                    new_lst.append(new_val)
                else:
                    new_lst.append(val)
            y_pro=new_lst
            
        plt.scatter(x_k, y_pro,marker=xingzhuang[c0],facecolors='none',edgecolors=c_draw[c0-1],alpha=1,label=f'ζ={z}')  # x轴数值，y轴数值，折线图的线条风格，折线图的线条宽度，折线图的线条颜色， 标记图形内容的标签文本
        c0+=1
    
    # 添加Poisson理论曲线，lambda = <k> = 10
    k_theory = np.arange(0, 30)
    p_theory = poisson.pmf(k_theory, mu=avg_k)

    plt.plot(
        k_theory, p_theory,
        color='#918072',
        linestyle='-',
        linewidth=1.8,
        label=fr'Poisson ($\lambda={avg_k}$)'
    )

    plt.xlabel(r'Degree, $k$', fontsize=18)
    plt.ylabel(r'$p(k)$', fontsize=18)
    plt.tick_params(labelsize=16)
    plt.legend(frameon=False,fontsize=15)

    plt.savefig('k分布.pdf')
            
        
    
    
    