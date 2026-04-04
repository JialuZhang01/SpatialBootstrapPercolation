# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:15:45 2025

@author: JialuZhang01
"""


import os 
import numpy as np
import matplotlib.pyplot as plt   
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker


def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)           

       
def draw_total(dic_zeta_pmax, dic_zeta_psecond, dic_zeta_pNOI, dic_zeta_psecond2,color_list, T_active, avg_k):
    """
    Generates a multi-panel figure to visualize percolation phase transitions.
    
    This function plots the order parameters (P_max, P_second, etc.) as a function 
    of the initial activation fraction (p) for different characteristic link lengths (zeta).

    """
    # Initialize a 3x2 Grid (Multi-panel layout)
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(6.8, 4.9),gridspec_kw={
        'height_ratios': [2, 1, 1]})
   
    
    # Column-wise Axis Sharing
    axs[1][0].sharex(axs[0][0])
    axs[2][0].sharex(axs[0][0])
    axs[1][1].sharex(axs[0][1])
    axs[2][1].sharex(axs[0][1])
    
    # Row-wise Axis Sharing:
    axs[0][1].sharey(axs[0][0])
    axs[1][1].sharey(axs[1][0])
    # axs[2][1].sharey(axs[2][0])
    
    # Redundancy Reduction
    axs[0][1].tick_params(axis='y', labelleft=False) 
    axs[1][1].tick_params(axis='y', labelleft=False) 
    axs[0][0].tick_params(axis='x', labelbottom=False)
    axs[0][1].tick_params(axis='x', labelbottom=False)
    axs[1][0].tick_params(axis='x', labelbottom=False) 
    axs[1][1].tick_params(axis='x', labelbottom=False)
    
    #  First line: Plot P∞(p)
    i = 0
    for zeta_pfin in dic_zeta_pmax:
        x1, y1 = zip(*dic_zeta_pmax[zeta_pfin].items())
         for zeta_pfin in dic_zeta_pmax:
        x1, y1 = zip(*dic_zeta_pmax[zeta_pfin].items())
        if zeta_pfin == zetas[0]:
            axs[0][0].plot(x1, y1, marker='o',linestyle='-',lw=1, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1], markersize=6,  label=f'ζ={zeta_pfin}')
           
        if zeta_pfin == zetas[1]:
            axs[0][0].plot(x1[28:], y1[28:], marker='o',linestyle='-',lw=1, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1], markersize=6,  label=f'ζ={zeta_pfin}')
           
        if zeta_pfin == zetas[2]:
            axs[0][0].plot(x1[40:], y1[40:], marker='o',linestyle='-',lw=1, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1], markersize=6,  label=f'ζ={zeta_pfin}')
            
            
        if zeta_pfin == zetas[3]:
            axs[0][1].plot(x1, y1, marker='o',linestyle='-', lw=1, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1], markersize=6,  label=f'ζ={zeta_pfin}')
            
        if zeta_pfin == zetas[4]:
            axs[0][1].plot(x1[26:], y1[26:], marker='o',linestyle='-', lw=1, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1], markersize=6,  label=f'ζ={zeta_pfin}')
            
        if zeta_pfin == zetas[5]:
            axs[0][1].plot(x1[40:], y1[40:], marker='o',linestyle='-', lw=1, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1], markersize=6,  label=f'ζ={zeta_pfin}')
        i += 1
    
    # Second line: Plot S_gc2(p)
    i = 0
    for zeta_psec in dic_zeta_psecond:
        x2, y2 = zip(*dic_zeta_psecond[zeta_psec].items())
        max_y2_index = np.argmax(y2)
        x_at_max_y2 = x2[max_y2_index]
        
        if zeta_psec == zetas[0]:
            axs[1][0].plot(x2, y2,linestyle='-',lw=2, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1])  
            axs[1][0].axvline(x=x_at_max_y2, color=color_list[i%3-1], linestyle=':')
          
        if zeta_psec == zetas[1]:
            axs[1][0].plot(x2, y2,linestyle='-',lw=2, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1])
            axs[1][0].axvline(x=x_at_max_y2, color=color_list[i%3-1], linestyle=':')
        
        if zeta_psec == zetas[2]:
            axs[1][0].plot(x2, y2,linestyle='-',lw=2, color=color_list[i%3-1], markerfacecolor='none',markeredgecolor=color_list[i%3-1])
            axs[1][0].axvline(x=x_at_max_y2, color=color_list[i%3-1], linestyle=':')
            
        if zeta_psec == zetas1[3]:
            axs[1][1].plot(x2, y2,linestyle='-', lw=2, color=color_list[i%3], markerfacecolor='none',markeredgecolor=color_list[i%3-1]) 
            axs[1][1].axvline(x=x_at_max_y2, color=color_list[i%3], linestyle=':')
           
        if zeta_psec == zetas1[4]:
            axs[1][1].plot(x2,y2,linestyle='-', lw=2, color=color_list[i%3], markerfacecolor='none',markeredgecolor=color_list[i%3-1])
            axs[1][1].axvline(x=x_at_max_y2, color=color_list[i%3], linestyle=':')
          
        if zeta_psec == zetas1[5]:
            axs[1][1].plot(x2, y2,linestyle='-', lw=2, color=color_list[i%3], markerfacecolor='none',markeredgecolor=color_list[i%3-1])
            axs[1][1].axvline(x=x_at_max_y2, color=color_list[i%3], linestyle=':')
        i += 1
    
    # Third row: Plot NOI(p) (with the y-axis on the right)
    i = 0
    for zeta_pN in dic_zeta_pNOI:
        x3, y3 = zip(*dic_zeta_pNOI[zeta_pN].items())
        max_y3_index = np.argmax(y3)
        x_at_max_y3 = x3[max_y3_index]

        if zeta_pN == zetas1[3]:
            axs[2][1].plot(x3, y3,linestyle='-', lw=2, color=color_list[i%3])
            axs[2][1].axvline(x=x_at_max_y3, color=color_list[i%3], linestyle='--')
           
        if zeta_pN == zetas1[4]:
            axs[2][1].plot(x3,y3,linestyle='-', lw=2, color=color_list[i%3])
            axs[2][1].axvline(x=x_at_max_y3, color=color_list[i%3], linestyle='--')
            
        if zeta_pN == zetas1[5]:
            axs[2][1].plot(x3,y3,linestyle='-', lw=2, color=color_list[i%3])
            axs[2][1].axvline(x=x_at_max_y3, color=color_list[i%3], linestyle='--')
        i += 1
       
    

     # Third row: Plot S_gc2^*(p) (with the y-axis on the left)
    i = 0
    for zeta_pN in dic_zeta_psecond2:
        x4, y4 = zip(*dic_zeta_psecond2[zeta_pN].items())
        max_y4_index = np.argmax(y4)
        x_at_max_y4 = x4[max_y4_index]
        if zeta_pN == zetas[0]:
            axs[2][0].plot(x4, y4,linestyle='-',lw=2, color=color_list[i%3-1]) 
            axs[2][0].axvline(x=x_at_max_y4, color=color_list[i%3-1], linestyle='--')
           
        if zeta_pN == zetas[1]:
            axs[2][0].plot(x4, y4,linestyle='-',lw=2, color=color_list[i%3-1])
            axs[2][0].axvline(x=x_at_max_y4, color=color_list[i%3-1], linestyle='--')
           
        if zeta_pN == zetas[2]:
            axs[2][0].plot(x4, y4,linestyle='-',lw=2, color=color_list[i%3-1]) 
            axs[2][0].axvline(x=x_at_max_y4, color=color_list[i%3-1], linestyle='--')
        i += 1
    
    #  Set the font size of the scale
    axs[0][0].set_ylim(top=1)
    axs[0][0].tick_params(axis='y', labelsize=10)  
    axs[1][0].tick_params(axis='y', labelsize=10)
    axs[2][0].tick_params(axis='y', labelsize=10)
    axs[2][1].tick_params(axis='y', labelsize=10)
    axs[2][0].tick_params(axis='x', labelsize=10)
    axs[2][1].tick_params(axis='x', labelsize=10)
    axs[2][1].yaxis.tick_right()
    def format_tick(value, pos):
        if value == 1000:
            return r'$10^3$' 
        else:
            return f'{value}'

    axs[2][1].yaxis.set_major_formatter(ticker.FuncFormatter(format_tick))
    
   # Set the labels 
    axs[2][0].set_xlabel('p', fontsize=12)
    axs[2][1].set_xlabel('p', fontsize=12)
    
    axs[0][0].set_ylabel('$P_\infty(p)$', fontsize=12)
    axs[1][0].set_ylabel('$S_{gc2}(p)$', fontsize=12)
    axs[2][0].set_ylabel('$S^*_{gc2}(p)$', fontsize=12)
    axs[2][1].set_ylabel(r'$\tau$', fontsize=12)
    axs[2][1].yaxis.set_label_position('right') 
    
    plt.tight_layout()

    path_line = 'deal_result/FIG1/'  
    mkdirectory(path_line)
    plt.savefig(f"{path_line}T={T_active}_avgk={avg_k}.pdf", dpi=300, bbox_inches='tight')
    plt.show()
            
    return 

def extract_info(z, deal_resultfile, source_pro1, source_pro2):
     """
    Parses a consolidated result file and maps zeta-p pairs to their respective metrics.
    
    The function uses an adaptive filtering logic: it applies different p-value 
    subsets (narrow or wide) depending on the magnitude of the zeta parameter.

    Parameters:
        zeta_list (list): The full list of spatial parameters (zeta) to include.
        result_filepath (str): Path to the processed data file.
        p_range_narrow (list): Activation fractions for high-spatial regimes (low zeta).
        p_range_wide (list): Activation fractions for long-range regimes (high zeta).

    Returns:
        dict: A structured dictionary {zeta: {p: value}}.
    """
    f = open(deal_resultfile, 'r', encoding='utf-8-sig')
    dic_zeta_p = {}  
    for zeta in z:
        dic_zeta_p[zeta] = {}
    
    for line in f:
        line = line.strip().split('\t')
        if not line or len(line) < 3: 
            continue
            
        try:
            zeta_val = int(line[0][4:])  
            p_val = float(line[1][1:])  
            data_val = float(line[2])   
          
            if zeta_val in z[:3] and p_val in source_pro1:
                dic_zeta_p[zeta_val][p_val] = data_val
            elif zeta_val in z[3:] and p_val in source_pro2:
                dic_zeta_p[zeta_val][p_val] = data_val
        except (ValueError, IndexError) as e:
            print(f"解析行时出错: {line}, 错误: {e}")
            continue
            
    f.close()
    return dic_zeta_p


def extract_info1(z, deal_resultfile, source_pro1, source_pro2):
    """
    Parses a consolidated result file and maps zeta-p pairs to their respective metrics.
    
    The function uses an adaptive filtering logic: it applies different p-value 
    subsets (narrow or wide) depending on the magnitude of the zeta parameter.

    Parameters:
        zeta_list (list): The full list of spatial parameters (zeta) to include.
        result_filepath (str): Path to the processed data file.
        p_range_narrow (list): Activation fractions for high-spatial regimes (low zeta).
        p_range_wide (list): Activation fractions for long-range regimes (high zeta).

    Returns:
        dict: A structured dictionary {zeta: {p: value}}.
    """
    f = open(deal_resultfile, 'r', encoding='utf-8-sig')
    dic_zeta_p = {} 
    for zeta in z:
        dic_zeta_p[zeta] = {}
    
    for line in f:
        line = line.strip().split('\t')
        if not line or len(line) < 3:  
            continue
            
        try:
            zeta_val = int(line[0][4:])  
            p_val = float(line[1][1:])   
            data_val = float(line[2])    
            
           
            if zeta_val in z[:3] and p_val in source_pro1:
                dic_zeta_p[zeta_val][p_val] = data_val
            elif zeta_val in z[3:] and p_val in source_pro2:
                dic_zeta_p[zeta_val][p_val] = data_val
        except (ValueError, IndexError) as e:
            print(f"解析行时出错: {line}, 错误: {e}")
            continue
            
    f.close()
    return dic_zeta_p

def extract_info2(z, resultfile_3, resultfile_4,resultfile_5,source_pro):
    """
    Aggregates statistical results from multiple files into a unified dictionary.

    Parameters:
        z_list (list): List of zeta values (spatial parameters).
        res_file_3/4/5 (str): Paths to the summary data files.
        source_pro (list): The specific initial activation fractions to filter for.

    Returns:
        dict: A nested dictionary structure {zeta: {p_fraction: measured_value}}.
    """
    dic_zeta_p = {} 
    for zeta in z[:3]:
        dic_zeta_p[zeta] = {}
    f = open(resultfile_3, 'r', encoding='utf-8-sig')
    for line in f:
        line = line.strip().split('\t')
        if float(line[0][1:]) in source_pro:
            dic_zeta_p[3][float(line[0][1:])] = float(line[3])
    f.close()
    f = open(resultfile_4, 'r', encoding='utf-8-sig')
    for line in f:
        line = line.strip().split('\t')
        if float(line[1][1:]) in source_pro:
            dic_zeta_p[4][float(line[1][1:])] = float(line[4])
    f.close()
    f = open(resultfile_5, 'r', encoding='utf-8-sig')
    for line in f:
        line = line.strip().split('\t')
        if float(line[1][1:]) in source_pro:
            dic_zeta_p[5][float(line[1][1:])] = float(line[4])
    f.close()
    return dic_zeta_p
        
        
        
    
    
    
    
    
if __name__ == "__main__":
    zetas = [5, 4, 3, 1000, 12, 6]  # The list of zeta values
    zetas1=[5,4,3,12,6,1000]
    avg_k = 10                      # Average Degree
    T_active = 6                    #  The activation threshold (T)
    
    #  The range of initial activation fractions
    source_pro1 = [x / 1000 for x in range(100, 286)]  # continuous phase transition
    source_pro2 = [x / 1000 for x in range(70, 321)]   # discontinuous phase transition
    
    # Color list
    color_list = ['#1072BD', '#77AE43', '#D7592C']
    
    # Read the file
    deal_resultfile1 = f'deal_result/T={T_active}_avgk={avg_k}_max_connexted.txt' 
    dic_zeta_pmax = extract_info(zetas, deal_resultfile1, source_pro1, source_pro2)
    deal_resultfile2 = f'deal_result/T={T_active}_avgk={avg_k}_second_connexted.txt'
    dic_zeta_psecond = extract_info1(zetas1, deal_resultfile2, source_pro1, source_pro2)
    deal_resultfile3 = f'deal_result/T={T_active}_avgk={avg_k}_NOI.txt'
    dic_zeta_pNOI = extract_info1(zetas1, deal_resultfile3, source_pro1, source_pro2)
    deal_resultfile0_3 =  f'deal_result/T={T_active}_avgk={avg_k}_max_connexted3_inactive.txt' 
    deal_resultfile0_4 =  f'deal_result/T={T_active}_avgk={avg_k}_max_connexted4_inactive.txt' 
    deal_resultfile0_5 =  f'deal_result/T={T_active}_avgk={avg_k}_max_connexted5_inactive.txt' 
    dic_zeta_psecond2 = extract_info2(zetas, deal_resultfile0_3,deal_resultfile0_4,deal_resultfile0_5,source_pro1)

    draw_total(dic_zeta_pmax, dic_zeta_psecond, dic_zeta_pNOI,dic_zeta_psecond2, color_list, T_active, avg_k)
    
    
    
