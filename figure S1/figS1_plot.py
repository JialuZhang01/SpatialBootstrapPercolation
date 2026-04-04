# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os 
import numpy as np
import matplotlib.pyplot as plt   


def mkdirectory(path):   
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)           


if __name__ == "__main__":
    zetas = [3,4,5,6,12,1000]  # The list of zeta values
    avg_k = 10    #  Average Degree
    i = 0  # Network ID
    source_pro =[x / 1000 for x in range(100, 286)]   # The range of initial activation fractions
    T_active = 8    #  The activation threshold (T)
  
   
    color_list = ['#77AE43','#1072BD','#EDB021','#D7592C','#7F318D','#ac1f18']
    dic_zeta_p = {}  #  key: zeta,value:{p*：P∞,p*:**,....,}
    for z in zetas:
        deal_resultfile = 'T='+str(T_active)+'/T='+str(T_active)+'_avgk='+str(avg_k)+'_max_connexted'+str(z)+'.txt'  
        f = open(deal_resultfile,'r',encoding='utf-8-sig')
       
        dic_zeta_p[z] = {}
        for line in f:
            line = line.strip().split('\t')
            dic_zeta_p[int(line[0][4:])][float(line[1][1:])]=float(line[2])  
        f.close()
    fig, ax = plt.subplots()
    i = 0
    for zeta_pfin in dic_zeta_p:
        x1, y1 = zip(*dic_zeta_p[zeta_pfin].items())
        plt.plot(x1, y1, marker='o',linestyle='-', lw=1, color=color_list[i], markerfacecolor='none',markeredgecolor=color_list[i], markersize=6,  label=f'ζ={zeta_pfin}')
        i += 1
    plt.legend()
    plt.title('T='+str(T_active)+'_'+'avgk='+str(avg_k))
    plt.xlabel('p',fontsize=18)
    plt.ylabel('$P_\infty(p)$',fontsize=18)   
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)



    path_line = 'T='+str(T_active)+'/fig_S1/'  
    mkdirectory(path_line)
    plt.savefig(path_line+'T='+str(T_active)+'_'+'avgk='+str(avg_k)+'_compare.pdf')
    plt.show()
                

            
    
   
    
    
    
    
    
    
    
