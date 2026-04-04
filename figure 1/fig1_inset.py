# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import numpy as np
import pickle as pk 
import matplotlib.pyplot as plt
import copy
import ast
import networkx as nx



def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    
       
if __name__ == "__main__":
    zetas = [1000]  # zeta
    avg_k = 10   # Average Degree
    i = 0
    T_active = 6  # The activation threshold (T)
    sim_time =10
    
    dic_sim_p= {}  # sim:{p:pinf} 
    for i in range(sim_time):
        dic_sim_p[i] ={}
        
    sim_pc2 = {}  # Record each simulation, sim:pc2
    f2 =open('deal_result/p_c-p_Pinf/sim_p_pinf.txt','r',encoding='utf-8-sig')
    for p0 in f2:
        p0 = p0.strip().split('\t')
        for i in p0[1:]:
            i = i.strip().split(',')
            dic_sim_p[int(p0[0][3:])][float(i[0])] = float(i[1])     
    f2.close()
    for i in dic_sim_p:
        pc2 = max(dic_sim_p[i])
        sim_pc2[i] =pc2
    sim_pc2_re = {}  #  The point on the left side of the PC is taken as the reference point
    for i in sim_pc2:
        pc2_re = round(sim_pc2[i]-0.0001,10)
        sim_pc2_re[i] =pc2_re
 
        
    dic_sim_cha ={}
    for i in range(sim_time):
        dic_sim_cha[i] ={}
    for i in dic_sim_p:
        for j in dic_sim_p[i]:
            if j < sim_pc2_re[i]:
                pc_cha = round(sim_pc2_re[i]-j,10)
                pinf_cha = round(dic_sim_p[i][sim_pc2_re[i]]-dic_sim_p[i][j],10)
                if (pc_cha > 0.0003):
                    dic_sim_cha[i][pc_cha] = pinf_cha
        
    fig, ax = plt.subplots(figsize=(5,5))
    dic_p_cha ={}
    x_average = []
    y_average = []
    for i in dic_sim_cha:
        for j in dic_sim_cha[i]:
            if j not in dic_p_cha:
                dic_p_cha[j] = []
            dic_p_cha[j].append(dic_sim_cha[i][j])
    for i in dic_p_cha:
        x_average.append(i)
        y_average.append(sum(dic_p_cha[i])/sim_time)
            
    
    
    
    y_0 = []
   
    for x_a in x_average:
        y_0.append(0.67*(x_a**(1/2)))
    ax.loglog(x_average, y_0,ls='-', lw=1, color='#D7592C', alpha = 1,label='β=1/2')     
    ax.scatter(x_average, y_average, facecolors='none',edgecolors='#D7592C',s=320)    
    
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')
    ax.set_ylabel('$P_\infty(p_c) - P_\infty(p)$',fontsize=35)  

    plt.legend(fontsize=24,loc='upper left',frameon=False)
    # Set the horizontal axis to logarithmic scale
    plt.xscale('log') 
    plt.yscale('log')  
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)

    
    # Hide the top and right borders.
    ax = plt.gca() 
    ax.spines['top'].set_visible(False)  
    ax.spines['left'].set_visible(False)  
    ax.spines['bottom'].set_visible(True)
    ax.spines['right'].set_visible(True)
    plt.xlabel('$p_c - p$',fontsize=35) 
    
    
    path_line = 'deal_result/' 
    mkdirectory(path_line)
    plt.savefig(path_line+'zeta='+str(zetas[0])+'_T='+str(T_active)+'_'+'avgk='+str(avg_k)+'_标度_fig1b-inset.pdf')
    plt.show()
    
    
    
    


 
    
    
            
        
                
            
            
    
    
    
    
    
