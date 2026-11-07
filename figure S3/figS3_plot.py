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

    path_line = 'FigS3/'
    mkdirectory(path_line)
    plt.savefig(f'{path_line}T2_T4_T8_avgk={avg_k}_pc.pdf', bbox_inches='tight')
    
   
    plt.tight_layout()
    plt.show()



def read_info(file_path):
    result = {}
    with open(file_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            z_str, v_str = line.split(",")
            zeta = int(z_str)
            val = float(v_str)
            result[zeta] = val
    return result



if __name__ == "__main__":
    zetas = [3,4,5,6,7,8,9,10,12,15,20,30,40,50,100,500,1000]   # The list of zeta values
    avg_k = 10   #  Average Degree
    sim_time = 10
    i=0
    
    T2_data = read_info("deal_result/T2_data.txt")
    T4_pc2_data = read_info("deal_result/T4_pc2_data.txt")
    T4_pc1_data = read_info("deal_result/T4_pc1_data.txt")
    T8_data = read_info("deal_result/T8_data.txt")
    draw_combined(T2_data, T4_pc1_data, T4_pc2_data, T8_data, avg_k)
