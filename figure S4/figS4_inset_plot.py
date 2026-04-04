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
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def linear_func(x, k, b):
    """Standard linear model: y = k*x + b"""
    return k * x + b

if __name__ == "__main__":
    L = 1000  # # Lattice length
    N = L * L  # Number of nodes

    zeta_l = [10,12,15,20,30] # The list of zeta values
    c_list  =['#5B423A','#1072BD','#EDB021','#D7592C','#7F318D']
    c_index=0
    v = []
    # plt.figure(figsize=(18, 5)) 
    for z in zeta_l:
        f = open('deal_result_rg变化/T=6/zeta='+str(z)+'/t_radius.txt','r',encoding='utf-8-sig')
        t = []
        r = []
        
        for i in f:
            i = i.strip().split('\t')     
            t.append(int(i[0][1:]))
            r.append(math.sqrt(float(i[1])))   
        f.close()
        
        # Extract the data from the rapidly rising period
        if z == 10:
            a,b = 200,300
        if z == 12:
            a,b = 200,220
           
        if z == 15:
            a,b = 150,200
           
        if z==20:
            a,b=140,200
           
        if z==30:
            a,b=120,150

        t_fast = t[a:b] # t=a~b
        r_fast = r[a:b]
            
      
        # Fit data within the rapid-growth interval to extract spreading dynamics
        popt_linear, _ = curve_fit(linear_func, t_fast, r_fast)
        # k_fit: the average propagation velocity (v); b_fit : the intercept
        k_fit, b_fit = popt_linear
        v.append(k_fit)
                

    
    ax = plt.gca()  
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.plot(zeta_l, v, marker='o',ls='-',lw=1,color=c_list[0],markersize=12,   
    markeredgecolor=c_list[0],  
    markerfacecolor='none')       
    plt.plot(zeta_l, v,color=c_list[0]) 
    plt.xticks(zeta_l, fontsize=20)  
    plt.yticks(fontsize=20)
    plt.xlabel(r'ζ', fontsize=26)
    plt.ylabel(r'$v$', fontsize=26)
    plt.legend(frameon=False,fontsize=16,ncol=1)
    plt.savefig('deal_result_rg/figS4_inset.pdf')
    plt.tight_layout()
    plt.show()

        
    
    
    
  
    
   
    
  
            


























        
        
