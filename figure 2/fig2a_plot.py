# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import matplotlib.pyplot as plt


def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def draw(dic_pc1, dic_pc2, dic_noi):
    """
    Plots the dependence of critical thresholds and peak activation times on the 
    spatial interaction range (zeta).

    Parameters:
        dic_pc1 (dict): First critical threshold p_c^(1) vs zeta.
        dic_pc2 (dict): Second critical threshold p_c^(2) vs zeta.
        dic_tau_max (dict): Maximum cascade duration (time step) vs zeta.
    """
    color_list = ['#1072BD', '#77AE43', '#D7592C', '#7F318D']
    fig, (ax1, ax2,ax3) = plt.subplots(3,1, figsize=(6, 6), sharex=True)
   

    pc2_x = sorted(dic_pc2.keys())
    pc2_y = [dic_pc2[x] for x in pc2_x]

    ax1.plot(list(dic_pc1.keys()), list(dic_pc1.values()), color=color_list[0], linestyle='-', linewidth=2.2, markersize=8, label='$p_c^{(1)}$')
    ax1.scatter(list(dic_pc1.keys()), list(dic_pc1.values()), facecolors='none', edgecolors=color_list[0], marker='o',s=48) 
   
    if len(pc2_x) >= 4:
       ax2.plot(pc2_x, pc2_y, color=color_list[1], linestyle='-', linewidth=2.2,markersize=8,label='$p_c^{(2)}$')
    else:
       ax2.plot(pc2_x, pc2_y, color=color_list[1], linestyle='-', linewidth=2.2)
    ax2.scatter(pc2_x, pc2_y, facecolors='none', edgecolors=color_list[1], marker='o',s=48)
    
   
    ax1.set_ylim(0.08, 0.17)
    ax1.set_yticks([0.1,0.13,0.16])
    ax2.set_ylim(0.215, 0.255) 
    ax1.set_ylabel('$p_c^{(1)}$',fontsize=14)
    ax1.tick_params(axis='y',labelsize=12)
    ax2.set_ylabel('$p_c^{(2)}$',fontsize=14)
    ax2.tick_params(axis='y',labelsize=12)
   
    noi_x = sorted(dic_noi.keys())
    noi_y = [dic_noi[x] for x in noi_x]

    ax3.plot(noi_x, noi_y, color=color_list[2], linestyle='-', linewidth=2.2,markersize=8, label='$ζ_c=6$')
    ax3.scatter(noi_x, noi_y, facecolors='none', edgecolors=color_list[2], marker='o',s=48)
    ax3.set_ylim(0,2700)
    ax3.set_yticks([0, 2000])  
    ax3.legend(ncol=1,fontsize=12,loc='best',frameon=True)
   
    max_noi_value = max(noi_y)
    max_noi_idx = noi_y.index(max_noi_value) 
    max_noi_x = noi_x[max_noi_idx]  
    
    ax2.axvline(x=max_noi_x, color='#888888', linestyle='--', linewidth=2.2, alpha=0.8)
    ax3.axvline(x=max_noi_x, color='#888888', linestyle='--', linewidth=2.2, alpha=0.8)
   
    ax3.set_xlabel('ζ',fontsize=14)
    ax3.set_ylabel(r'$\tau_{\max}$',fontsize=14)
    ax3.tick_params(axis='x',labelsize=12)
    
    ax3.tick_params(axis='y', labelsize=12)  
    ax3.legend(fontsize=12)

    ax1.set_xscale('log') 
    ax3.set_xscale('log')  
    

    plt.subplots_adjust(hspace=0)
    path_line = 'deal_result/' 
    mkdirectory(path_line)
   
    plt.savefig(path_line + 'fig_2a.pdf')
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
            
    return dic_zeta_pc1, d_zeta_pc1


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
        
        if (zeta == 3) or (zeta == 4) or (zeta == 5):
            f_NOI = open('deal_result/pc2/' + 'T=' + str(T_active) + '_avgk=' + str(avg_k) + '_inactive_gc2_' + str(zeta) + '.txt', 'r', encoding='utf-8-sig')
            for line in f_NOI:
                line = line.strip().split('\t')
                for sim_t in range(sim_time):
                    dic_zeta_sim[int(line[0][4:])][sim_t][float(line[1][1:])] = int(line[2 + sim_t])
            f_NOI.close()
        else:
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
            
    return dic_zeta_pc2, d_zeta_pc2

def identify_noi(i, zetas, avg_k, T_active, sim_time): 
    """
    Identifies the peak activation intensity (NOI) across different spatial ranges.

    Parameters:
        net_id (int): Network identifier.
        zetas (list): List of spatial interaction ranges.
        avg_k (float): Average degree.
        T_active (int): Activation threshold.
        sim_time (int): Number of independent realizations.

    Returns:
        raw_noi_dict, mean_peak_noi_dict
           
    """
    
    dic_zeta_sim = {}  
    
    for zeta in zetas:
        dic_zeta_sim[zeta] = [{} for s in range(sim_time)]
        
        f_NOI = open('deal_result/pc2/' + 'T=' + str(T_active) + '_avgk=' + str(avg_k) + '_NOI_' + str(zeta) + '.txt', 'r', encoding='utf-8-sig')
        for line in f_NOI:
            line = line.strip().split('\t')
            for sim_t in range(sim_time):
                dic_zeta_sim[int(line[0][4:])][sim_t][float(line[1][1:])] = int(line[2 + sim_t])
        f_NOI.close()
           
    dic_zeta_noi = {}    
    for zeta in zetas:
        dic_zeta_noi[zeta] = []
    for z in dic_zeta_sim:
        for i in dic_zeta_sim[z]:
            max_n = max(i.values())
            dic_zeta_noi[z].append(max_n)
   
    d_zeta_noi = {}
    for zeta in zetas:
        d_zeta_noi[zeta] = 0
    for x in dic_zeta_noi:
        ave = sum(dic_zeta_noi[x]) / len(dic_zeta_noi[x])
        d_zeta_noi[x] = round(ave, 4)    
            
    return dic_zeta_noi, d_zeta_noi


if __name__ == "__main__":
  
    zetas = [3,4,5,6,7,8,9,10,12,15,20,30,40,50,100,500,1000]   # # The list of zeta values
    avg_k = 10   #  Average Degree
    i = 0
    T_active = 6  # The activation threshold (T)
    sim_time = 10
   
    Dic_zeta_pc1, D_zeta_pc1 = identify_pc1(i, zetas, avg_k, T_active, sim_time)
    Dic_zeta_pc2, D_zeta_pc2 = identify_pc2(i, zetas, avg_k, T_active, sim_time)
    Dic_zeta_noi, D_zeta_noi = identify_noi(i, zetas, avg_k, T_active, sim_time)
    draw(D_zeta_pc1, D_zeta_pc2, D_zeta_noi)
    
