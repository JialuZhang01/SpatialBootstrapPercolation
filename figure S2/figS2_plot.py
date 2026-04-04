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

def draw_combined(T2_data, T4_pc1_data, T4_pc2_data, T8_data, avg_k):
    """
    compare critical thresholds across different activation requirements (T=2, 4, 8).

    Parameters:
        T2_data (dict): Critical thresholds for T=2 .
        T4_pc1_data, T4_pc2_data (dict): Primary and secondary thresholds for T=4.
        T8_data (dict): Critical thresholds for T=8.
        avg_k (int):# Average Degree
    """
    
    color_list = ['#77AE43','#1072BD','#D7592C','#7F318D']
    
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 5.8), sharex=True)
    fig.subplots_adjust(hspace=0.3)  

    # ---------------------- T=2 ----------------------
    ax1.plot(list(T2_data.keys()), list(T2_data.values()), 
             color=color_list[0], linestyle='-', linewidth=2, markersize=8, label='$p^2_{c}$')
    ax1.scatter(list(T2_data.keys()), list(T2_data.values()), 
                facecolors='none', edgecolors=color_list[0], marker='o')
    ax1.set_ylabel('$p_c$',fontsize=12)
    ax1.set_title('T=2', fontsize=15)
    ax1.set_ylim(-0.0005,0.0058)
    # ax1.set_yticks(0,0.002,0.004)
    ax1.tick_params(axis='both', labelsize=12)

    # ---------------------- T=4 ----------------------
    ax2.plot(list(T4_pc1_data.keys()), list(T4_pc1_data.values()), 
             color=color_list[1], linestyle='-', linewidth=2, markersize=8, label='$p_c^{(1)}$')
    ax2.scatter(list(T4_pc1_data.keys()), list(T4_pc1_data.values()), 
                facecolors='none', edgecolors=color_list[1], marker='o')
    ax2.plot(list(T4_pc2_data.keys()), list(T4_pc2_data.values()), 
             color=color_list[0], linestyle='-', linewidth=2, markersize=8, label='$p_c^{(2)}$')
    ax2.scatter(list(T4_pc2_data.keys()), list(T4_pc2_data.values()), 
                facecolors='none', edgecolors=color_list[0], marker='o')
    ax2.set_ylabel('$p_c$',fontsize=12)
    ax2.set_title('T=4', fontsize=15)
    ax2.set_ylim(0.02,0.1)
    ax2.legend(loc='lower right', fontsize=11,ncol=2,frameon=False)
    ax2.tick_params(axis='both', labelsize=12)

    # ---------------------- T=8 ----------------------
    ax3.plot(list(T8_data.keys()), list(T8_data.values()), 
             color=color_list[1], linestyle='-', linewidth=2, markersize=8, label='$p^1_{c}$')
    ax3.scatter(list(T8_data.keys()), list(T8_data.values()), 
                facecolors='none', edgecolors=color_list[1], marker='o')
    ax3.set_ylabel('$p_c$',fontsize=12)
    ax3.set_xlabel('ζ',fontsize=12)  
    ax3.set_title('T=8', fontsize=15)
    ax3.set_ylim(0.09,0.2)
    ax3.tick_params(axis='both', labelsize=12)

    
    ax3.set_xscale('log')

    path_line = 'FigS2/'
    mkdirectory(path_line)
    plt.savefig(f'{path_line}T2_T4_T8_avgk={avg_k}_pc.pdf', bbox_inches='tight')
    
   
    plt.tight_layout()
    plt.show()


def identify_pc1(i, zetas, avg_k, T_active, sim_time):  
    """
    Identifies the first critical threshold (p_c1) based on the peak of the 
    second largest connected component (S_gc2).

    The critical point is determined by finding the initial activation fraction 'p' 
     that maximizes the susceptibility-like indicator (size of the second largest cluster)
    across multiple simulation realizations.

    Parameters:
        net_id (int): Network identifier.
        zetas (list): List of spatial interaction ranges.
        avg_k (int): Average degree of the network.
        T_active (int): Activation threshold.
        sim_time (int): Number of independent simulation realizations.

    Returns:
        raw_pc1_dict, mean_pc1_dict
               - raw_pc1_dict: {zeta: [pc1_run1, pc1_run2, ...]}
               - mean_pc1_dict: {zeta: ensemble_average_pc1}
    """
    dic_zeta_sim = {}  
    
    for zeta in zetas:
        dic_zeta_sim[zeta] = [{} for s in range(sim_time)]
        
        f_gc2 = open('deal_result/pc1/' + 'T=' + str(T_active) + '_avgk=' + str(avg_k) + '_second_connexted_' + str(zeta) + '.txt', 'r', encoding='utf-8-sig')
        for line in f_gc2:
            line = line.strip().split('\t')
            for sim_t in range(sim_time):
                dic_zeta_sim[int(line[0][4:])][sim_t][float(line[1][1:])] = float(line[2 + sim_t])
        f_gc2.close()
        
    dic_zeta_pc1 = {}   
    
    for zeta in zetas:
        dic_zeta_pc1[zeta] = []
    for z in dic_zeta_sim:
        for i in dic_zeta_sim[z]:
            max_p = max(i, key=i.get)
            dic_zeta_pc1[z].append(max_p)
            
    d_zeta_pc1 = {}
    for zeta in zetas:
        d_zeta_pc1[zeta] = 0
    for x in dic_zeta_pc1:
        ave = sum(dic_zeta_pc1[x]) / len(dic_zeta_pc1[x])
        d_zeta_pc1[x] = round(ave, 4)      
            
    return  d_zeta_pc1


def identify_pc2(i, zetas, avg_k, T_active, sim_time): 
    """
    Identifies the second critical threshold (p_c2) based on the peak of the 
    S_gc2^* or NOI.

    
    Parameters:
        net_id (int): Network identifier.
        zetas (list): List of spatial interaction ranges.
        avg_k (int): Average degree of the network.
        T_active (int): Activation threshold.
        sim_time (int): Number of independent simulation realizations.

    Returns:
        raw_pc2_dict, mean_pc2_dict
           
    """
    dic_zeta_sim = {}  
    for zeta in zetas:
        dic_zeta_sim[zeta] = [{} for s in range(sim_time)]
        
       
          f_gc = open('deal_result/pc2/' + 'T=' + str(T_active) + '_avgk=' + str(avg_k) + '_max_connexted' + str(zeta) + '.txt', 'r', encoding='utf-8-sig')
          for line in f_gc:
              line = line.strip().split('\t')
              for sim_t in range(sim_time):
                  dic_zeta_sim[int(line[0][4:])][sim_t][float(line[1][1:])] = float(line[2 + sim_t])
          f_gc.close()
           
    dic_zeta_pc2 = {}
    
    for zeta in zetas:
        dic_zeta_pc2[zeta] = []
    for z in dic_zeta_sim:
        if (z == 3) or (z == 4):
            for i in dic_zeta_sim[z]:
                max_p = max(i, key=i.get)
                dic_zeta_pc2[z].append(max_p)
        else:
            for i in dic_zeta_sim[z]:
                sorted_keys = sorted(i.keys())
                for j in range(1, len(sorted_keys)):
                    prev_key = sorted_keys[j-1]
                    current_key = sorted_keys[j]
                    diff = i[current_key] - i[prev_key]
                    if diff > 0.2:
                        dic_zeta_pc2[z].append(current_key)
                        break
     
    d_zeta_pc2 = {}
    for zeta in zetas:
        d_zeta_pc2[zeta] = 0
    for x in dic_zeta_pc2:
        ave = sum(dic_zeta_pc2[x]) / len(dic_zeta_pc2[x])
        d_zeta_pc2[x] = round(ave, 4)    
            
    return  d_zeta_pc2


if __name__ == "__main__":
    zetas = [3,4,5,6,7,8,9,10,12,15,20,30,40,50,100,500,1000]   # The list of zeta values
    avg_k = 10   #  Average Degree
    sim_time = 10
    i=0
  
    T8_data = identify_pc1(i, zetas, avg_k, T_active=8, sim_time)
    T2_data = identify_pc2(i, zetas, avg_k, T_active=2, sim_time)
    T4_pc1_data = identify_pc1(i, zetas, avg_k, T_active=4, sim_time)
    T4_pc2_data = identify_pc2(i, zetas, avg_k, T_active=4, sim_time)
    
    
    draw_combined(T2_data, T4_pc1_data, T4_pc2_data, T8_data, avg_k)
