# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 10:27:52 2025

@author: JialuZhang01
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

L_size = 500   # Lattice length
T_active = 6  # The activation threshold (T)
zetas = [z for z in range(4,51)]   # Range of zeta values
avg_k_list  = [a_k / 10 for a_k in range(100, 151)]  #  List of Average Degree
dic_zeta_avgk = {}

for zeta in zetas:
    dic_zeta_avgk[zeta] ={}
    f = open('deal_result/avgk_rc/zeta='+str(zeta)+'_k_rc.txt','r',encoding='utf-8-sig')
    for line in f:
        line= line.strip().split('\t')
        k0 = float(line[0][3:])
        dic_zeta_avgk[zeta][k0]=int(line[1])
    f.close()
        

row_labels = sorted(list(set(key for inner_dict in dic_zeta_avgk.values() for key in inner_dict.keys())), reverse=True) 
col_labels = sorted(dic_zeta_avgk.keys())

matrix = np.zeros((len(row_labels), len(col_labels)))  

# 填充矩阵值
for i, row in enumerate(row_labels):
    for j, col in enumerate(col_labels):
        if row in dic_zeta_avgk[col]:
            matrix[i, j] = dic_zeta_avgk[col][row]

plt.figure(figsize=(8, 3.6))

# Use seaborn to create a heatmap
ax = sns.heatmap(
    matrix,                
    annot=False,          
    fmt=".0f",              
    cmap="viridis",         
    cbar_kws={"label": "$r_c$"},
    linewidths=0,  
    annot_kws={"size": 16}, 
    cbar=True,               
    square=True,             
    xticklabels=col_labels, 
    yticklabels=row_labels  
)

cbar = ax.collections[0].colorbar
cbar.ax.set_ylabel(
    "$r_c$",  
    fontsize=12 
)


for i, label in enumerate(ax.get_xticklabels()):
    if i % 5 != 1: 
        label.set_visible(False)
        
for i, label in enumerate(ax.get_yticklabels()):
    if i % 5 != 0: 
        label.set_visible(False)
        

plt.title("L=500,T=6", fontsize=14)

    
plt.xlabel("ζ", fontsize=14)
plt.ylabel(r"$\langle k \rangle$", fontsize=14)

plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('deal_result/L='+str(L_size)+'_T='+str(T_active)+'_heatmap.pdf')
plt.show()








