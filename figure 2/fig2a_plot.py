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
        
        
def read_info(avg_k,T_active):
    dic_zeta_pc1={}
    f_pc1=open(f'deal_result/T{T_active}_avgk{avg_k}_pc1_final.txt','r',encoding='utf-8-sig')
    for line in f_pc1:
        line=line.strip().split('\t')
        dic_zeta_pc1[int(line[0][4:])]=float(line[1])
    f_pc1.close()
    dic_zeta_pc2={}
    f_pc2=open(f'deal_result/T{T_active}_avgk{avg_k}_pc2_final.txt','r',encoding='utf-8-sig')
    for line in f_pc2:
        line=line.strip().split('\t')
        dic_zeta_pc2[int(line[0][4:])]=float(line[1])
    f_pc2.close()
    dic_zeta_noi={}
    f_noi=open(f'deal_result/T{T_active}_avgk{avg_k}_noi_final.txt','r',encoding='utf-8-sig')
    for line in f_noi:
        line=line.strip().split('\t')
        dic_zeta_noi[int(line[0][4:])]=float(line[1])
    f_noi.close()
        
    
    return dic_zeta_pc1,dic_zeta_pc2,dic_zeta_noi

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
    path_line = 'FIG2/' 
    mkdirectory(path_line)
   
    plt.savefig(path_line + 'fig_2a.pdf')
    plt.tight_layout()
    plt.show()







if __name__ == "__main__":
  
    zetas = [3,4,5,6,7,8,9,10,12,15,20,30,40,50,100,500,1000]   # # The list of zeta values
    avg_k = 10   #  Average Degree
    i = 0
    T_active = 6  # The activation threshold (T)
    
   
    D_zeta_pc1,D_zeta_pc2,D_zeta_noi =read_info(avg_k,T_active)
    draw(D_zeta_pc1, D_zeta_pc2, D_zeta_noi)
    
