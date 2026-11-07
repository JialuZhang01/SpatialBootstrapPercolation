# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: Administor
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def mkdirectory(path):     
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def read_z_p_rc():
    dic_z_p_rc = {}
    with open("deal_result/z_p_rc.txt", "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            L0_str, z_str, p_str, val_str = line.split(',')
            L0 = int(L0_str)
            z = int(z_str)
            p = float(p_str)
            val = float(val_str)
            if L0 not in dic_z_p_rc:
                dic_z_p_rc[L0] = {}
            dic_z_p_rc[L0][z] = {p: val}
    return dic_z_p_rc
        

        
text_l=['b','c','d']
fig, axes = plt.subplots(
    nrows=1, ncols=3,
    figsize=(14.7, 4.2), 
    constrained_layout=True
)
    



for j0 in range(3): 
    ax = axes[j0]  
    if j0 == 0:   
        L_size = 500
        T_active = 6
        zetas = [z for z in range(3, 51)]  # 横轴：zeta
        source_p_list = [x / 1000 for x in range(85, 266)]  # 纵轴：p
        dic_zeta_p = {}
        
        # 读取数据
        for zeta in zetas:
            dic_zeta_p[zeta] = {}
            f = open(f'2.3.1_500_localized_seed/deal_result/source_p_rc/zeta={zeta}_p_rc.txt', 'r', encoding='utf-8-sig')
            for line in f:
                line = line.strip().split('\t')
                p0 = float(line[0][1:])
                if p0 in source_p_list:
                    dic_zeta_p[zeta][p0] = int(line[1])
            f.close()
     
    
        row_labels = sorted(list(set(key for inner_dict in dic_zeta_p.values() for key in inner_dict.keys())), reverse=True)
        col_labels = sorted(dic_zeta_p.keys())
        
    
        matrix = np.zeros((len(row_labels), len(col_labels)))
        for i, row in enumerate(row_labels):
            for j, col in enumerate(col_labels):
                if row in dic_zeta_p[col]:
                    matrix[i, j] = dic_zeta_p[col][row]
   
        step = 30
        y_tick_labels = [label if i % step == 0 else '' for i, label in enumerate(row_labels)]
        
        
        sns.heatmap(
            matrix,
            annot=False,
            fmt=".0f",
            cmap="viridis",
            cbar_kws={"label": "$r_c$"},
            linewidths=0,
            cbar=True,
            square=False,
            xticklabels=col_labels,
            yticklabels=y_tick_labels,
            ax=ax 
        )
        cbar = ax.collections[0].colorbar
        cbar.ax.set_ylabel("$r^c_h$", fontsize=17)
        
        for i, label in enumerate(ax.get_xticklabels()):
            if i % 15 != 1:
                label.set_visible(False)
        
        ax.set_xlabel("ζ", fontsize=17)
        ax.set_ylabel("p", fontsize=17)
        ax.tick_params(axis='x', labelsize=18, rotation=0)
        ax.tick_params(axis='y', labelsize=18, rotation=0) 
       
    if  j0 == 1:   
        l = [1500,1000,700,500]
        c0=0
        c_l=['#D7592C','#EDB021','#1072BD','#77AE43','#7F318D']
        
        source_p =[x/1000 for x in range(125,286)]
        for i in l:
            y = []
            f = open('deal_result/zeta=12_p_rc_'+str(i)+'.txt','r',encoding='utf-8-sig')
            for j in f:
                j = j.strip().split('\t')
                if float(j[0][1:]) in source_p:
                    y.append(int(j[1]))
                
                    
            diff = len(source_p) - len(y)
            if diff > 0:
                y += [0] * diff
            ax.plot(source_p[::1],y[::1],marker='o', markeredgewidth=0.6,markerfacecolor='none',color=c_l[c0], markeredgecolor=c_l[c0])
           
            c0+=1
            if i == 1500:
                for i00, val in enumerate(y):
                    if val != 750:
                        pos_x = source_p[i00]
                        pos_y = y[i00-1]
                        break
                for i11, val1 in enumerate(y):
                    if val1 == 0:
                        pos_x1 = source_p[i11]
                        break
        
        ax.set_xlim(0.12, 0.29)  
        ax.set_xticks([0.15, 0.20, 0.25])  
        ax.set_ylim(-50, 945)  
        ax.set_yticks(range(0, 801,400))  
        ax.set_xlabel('p',fontsize=17)
        ax.set_ylabel('$r_h^c$',fontsize=17)
  
    if j0 == 2:
        c0=0
        c_l=['#77AE43','#1072BD','#EDB021','#D7592C','#7F318D']
        l = [i for i in range(4,51)]
        source_p =0.2
        dic_z_p_rc = {}
        L_list = [500,700,1000,1500]
       
        dic_z_p_rc = read_z_p_rc()
        print(dic_z_p_rc)
        for L0  in L_list:
            print(L0)
            y = []  
            for i in dic_z_p_rc[L0]:
                y.append(dic_z_p_rc[L0][i][source_p]) 
         
            ax.plot(l,y,marker='o',markerfacecolor='none',markeredgewidth=0.6,label='L='+str(L0),color=c_l[c0], markeredgecolor=c_l[c0])
            c0+=1
        ax.set_ylim(-50, 945)     
        ax.set_yticks(range(0, 801,400))  
        ax.set_xlabel('ζ',fontsize=17)
        ax.set_ylabel('$r_h^c$',fontsize=17)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)

path_line = 'FIG5/' 
mkdirectory(path_line)
plt.savefig(path_line + 'fig_5.pdf')
plt.legend(frameon=False)
plt.show()






   



   
