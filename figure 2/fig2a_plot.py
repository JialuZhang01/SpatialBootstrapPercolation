# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: Administor
"""

import os
import matplotlib.pyplot as plt


def mkdirectory(path):     # 若文件夹不存在，建立它
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def draw(dic_pc1, dic_pc2, dic_noi):
    color_list = ['#1072BD', '#77AE43', '#D7592C', '#7F318D']
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True, gridspec_kw={'height_ratios': [33, 15]})
   
    pc2_x = sorted(dic_pc2.keys())
    pc2_y = [dic_pc2[x] for x in pc2_x]

    # 第一行子图：绘制pc1和pc2
    ax1.plot(list(dic_pc1.keys()), list(dic_pc1.values()), color=color_list[0], linestyle='-', linewidth=2.2, markersize=8, label='$p^1_c$')
    ax1.scatter(list(dic_pc1.keys()), list(dic_pc1.values()), facecolors='none', edgecolors=color_list[0], marker='o',s=120) 
    if len(pc2_x) >= 4:
       ax1.plot(pc2_x, pc2_y, color=color_list[1], linestyle='-', linewidth=2.2,markersize=8,label='$p^2_c$')
    else:
       ax1.plot(pc2_x, pc2_y, color=color_list[1], linestyle='-', linewidth=2.2)
    ax1.scatter(pc2_x, pc2_y, facecolors='none', edgecolors=color_list[1], marker='o',s=120)
    
    ax1.set_ylim(0.08, 0.26)
   
    
    ax1.set_ylabel('$p_c$',fontsize=24)
    ax1.tick_params(axis='y',labelsize=20)
    ax1.legend(ncol=1,fontsize=16,loc='best',frameon=True)
    

    noi_x = sorted(dic_noi.keys())
    noi_y = [dic_noi[x] for x in noi_x]

    # 绘制NOI
    ax2.plot(noi_x, noi_y, color=color_list[2], linestyle='-', linewidth=2.2,markersize=8)
    ax2.scatter(noi_x, noi_y, facecolors='none', edgecolors=color_list[2], marker='o',s=120)
    ax2.set_ylim(0,2700)
    ax2.set_yticks([0, 2000])  # 包含2000，同时保留0、1000、2700（范围上限）

   
    # 找到NOI最大值对应的x坐标（多个取第一个）
    max_noi_value = max(noi_y)
    max_noi_idx = noi_y.index(max_noi_value)  # 最大值的索引
    max_noi_x = noi_x[max_noi_idx]  # 对应的x坐标（zeta值）

    # 绘制贯穿两行子图的垂直线
    ax1.axvline(x=max_noi_x, color='#888888', linestyle='--', linewidth=2.2, alpha=0.8)
    ax2.axvline(x=max_noi_x, color='#888888', linestyle='--', linewidth=2.2, alpha=0.8)
   
    ax2.set_xlabel('ζ',fontsize=24)
    ax2.set_ylabel(r'$\tau_{\max}$',fontsize=24)
    ax2.tick_params(axis='x',labelsize=20)
    
    ax2.tick_params(axis='y', labelsize=20)  
    ax1.set_xscale('log')  
    ax2.set_xscale('log') 
    
    
    
    
    plt.subplots_adjust(hspace=0)  

    path_line = 'deal_result/' 
    mkdirectory(path_line)
    plt.savefig(path_line + 'T=' + str(T_active) + '_' + 'avgk=' + str(avg_k) + '_zeta_pc_NOI_fig2a.pdf')

    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()

def identify_pc1(i, zetas, avg_k, T_active, sim_time):  # Network ID,zeta,平均度,初始active的比例,阈值列表,模拟次数
    dic_zeta_sim = {}  # key为ζ，value为[{p1:S(gc2),p2:S(gc2),...},{同前}]
    
    for zeta in zetas:
        dic_zeta_sim[zeta] = [{} for s in range(sim_time)]
        
        f_gc2 = open('deal_result/pc1/' + 'T=' + str(T_active) + '_avgk=' + str(avg_k) + '_second_connexted_' + str(zeta) + '.txt', 'r', encoding='utf-8-sig')
        for line in f_gc2:
            line = line.strip().split('\t')
            for sim_t in range(sim_time):
                dic_zeta_sim[int(line[0][4:])][sim_t][float(line[1][1:])] = float(line[2 + sim_t])
        f_gc2.close()
        
    dic_zeta_pc1 = {}   #  key为ζ，value为[每一次的pc1]
    
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
        d_zeta_pc1[x] = round(ave, 4)     #保留的小数位，依照选取的精度和模拟次数 
            
    return dic_zeta_pc1, d_zeta_pc1

def identify_pc2(i, zetas, avg_k, T_active, sim_time):  # Network ID,zeta,平均度,初始active的比例,阈值列表,模拟次数
    dic_zeta_sim = {}  # key为ζ，value为[{p1:S(gc),p2:S(gc),...},{同前}],zeta=3,4的时候是NOI
    
    for zeta in zetas:
        dic_zeta_sim[zeta] = [{} for s in range(sim_time)]
        
        if (zeta == 3) or (zeta == 4) or (zeta == 5):
            f_NOI = open('deal_result/pc2/' + 'T=' + str(T_active) + '_avgk=' + str(avg_k) + '_NOI_' + str(zeta) + '.txt', 'r', encoding='utf-8-sig')
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

def identify_noi0(i, zetas, avg_k, T_active, sim_time):  # Network ID,zeta,平均度,初始active的比例,阈值列表,模拟次数
    dic_zeta_sim = {}  # key为ζ，value为[{p1:S(gc),p2:S(gc),...},{同前}],zeta=3,4的时候是NOI
    
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
    zetas = [3,4,5,6,7,8,9,10,12,15,20,30,40,50,100,500,1000]   # The list of zeta values
    avg_k = 10   # Average Degree
    i = 0
    T_active = 6  # The activation threshold (T)
    sim_time = 10
   
    Dic_zeta_pc1, D_zeta_pc1 = identify_pc1(i, zetas, avg_k, T_active, sim_time)
    Dic_zeta_pc2, D_zeta_pc2 = identify_pc2(i, zetas, avg_k, T_active, sim_time)
    Dic_zeta_noi, D_zeta_noi = identify_noi0(i, zetas, avg_k, T_active, sim_time)
    draw(D_zeta_pc1, D_zeta_pc2, D_zeta_noi)
    
