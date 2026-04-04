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
    L = 1000   # Lattice length
    N = L * L   # Number of nodes
    
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
       
        plt.plot(
            t, r,
            ls='-',         
            lw=1,          
            color=c_list[c_index],  
            alpha=1,         
            label=f'ζ={z}',   
            marker='o',     
            markersize=8,   
            markeredgecolor=c_list[c_index], 
            markerfacecolor='none',           
            # markeredgewidth=1,                
        )
        c_index+=1
        
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.xlabel(r't', fontsize=24)
    plt.ylabel(r'$R_g$', fontsize=24)
    # plt.title('branching process', fontsize=21)
    plt.legend(frameon=False,fontsize=18,ncol=1)
    plt.savefig('deal_result_rg/fig4c_.pdf')
    plt.tight_layout()
    plt.show()

        
    
    
    
  
    
   
    
  
            


























        
        
