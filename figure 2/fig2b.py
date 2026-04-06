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
from matplotlib.colors import ListedColormap


def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
 
       
if __name__ == "__main__":
    L_side = 1000   # Lattice length
    networkpath = 'network/'   # the network's path.  
    zeta = 12 
    source_p = 0.229  # pc2
    avg_k = 10   # Average degree
    i = 0
    T_active = 6  # The activation threshold (T)
    sim_time = 1
    deal_resultpath = 'deal_result/'
    deal_results_spatial =  deal_resultpath +'spatial_fig2.b/'+ f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/spatial_result_total/'
    
    # Define a custom colormap for the phase state: 
    #  Green (#5BAB54) for LCC nodes,Purple (#885F9C) for others.
    f1 = open('deal_result/3、12、1000_cascade_dynamic/'+'T='+str(T_active) +'_avgk='+str(avg_k) +'_t_S(gc)_nodes_zeta'+str(zeta)+'_'+str(source_p)+'.txt','r', encoding='utf-8-sig')
    t = 0
    for line_f1 in f1:
        line_f1 = line_f1.strip().split('\t')
        if line_f1[0] == 'p'+str(source_p):
            for i in line_f1[1:]: # i = [nodes in the LCC at time t0, nodes in the LCC at time t1, ...]
                color_matrix = np.zeros((L_side, L_side)) 
                lcc_nodes =[] 
                if i != 'null':  
                    i = i.strip().split(';')  
                    for n1 in i[0:-1]:  
                        lcc_nodes.append(ast.literal_eval(n1))   
                for i0, j0 in lcc_nodes:  
                    # color_matrix[int(i0-300)%L_side, int(j0+200)%L_side] = 1   # 12
                    color_matrix[int(i0), int(j0)] = 1
                    
                cmap = ListedColormap(['#885F9C', '#5BAB54'])  
                plt.imshow(color_matrix, cmap=cmap, origin='lower', vmin=0,vmax=1)
                plt.xticks([])
                plt.yticks([])
                plt.xlim(0, L_side)
                plt.ylim(0, L_side)
                plt.box(False)
                plt.title(f't={t}',fontsize=24)
                
                mkdirectory(deal_results_spatial+ str(0) + '_simulation/')  
                plt.savefig(deal_results_spatial+ str(0) + '_simulation/'+ 'step_'+ str(t)+'.pdf',bbox_inches = 'tight')
                plt.close()
                t+=1   
               
                print('t:'+str(t))
            break
    
    f1.close()
                

    
