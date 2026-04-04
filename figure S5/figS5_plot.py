# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import math
from math import exp, factorial

z = 10
T = 6

def Q_T(u):
    # Q_T(u) = 1 - sum_{k=0}^{T-1} e^{-u} u^k / k!
    s = 0.0
    for k in range(0, T):
        s += math.exp(-u) * (u**k) / math.factorial(k)
    return 1.0 - s



# Given S, compute p from derivative condition:
# (1-p) * z * e^{-u} u^{T-1} / (T-1)! = 1  => p = 1 - 1/denom
def p_from_S_by_derivative(S):
    u = z * S
    denom = z * math.exp(-u) * (u**(T-1)) / math.factorial(T-1)
    if denom <= 0:
        return None
    return 1.0 - 1.0 / denom


# Residual of self-consistency S = p + (1-p) Q_T(zS)
def residual(S):
    p = p_from_S_by_derivative(S)
    if p is None or not (0.0 < p < 1.0):
        return None
    u = z * S
    Q = Q_T(u)
    return S - (p + (1-p) * Q)

# scan S in (0,1) to find sign changes, then refine with bisection
Ss = np.linspace(1e-4, 0.9999, 20000)
vals = []
for s in Ss:
    r = residual(s)
    vals.append(r if r is not None else np.nan)

# find intervals where sign changes
intervals = []
for i in range(len(Ss)-1):
    a, b = Ss[i], Ss[i+1]
    ra, rb = vals[i], vals[i+1]
    if np.isnan(ra) or np.isnan(rb):
        continue
    if ra == 0.0:
        intervals.append((a,a))
    elif ra * rb < 0:
        intervals.append((a,b))

# refine first interval with bisection
def refine(a,b,eps=1e-8):
    fa = residual(a); fb = residual(b)
    if fa is None or fb is None:
        return None
    for _ in range(60):
        m = 0.5*(a+b)
        fm = residual(m)
        if fm is None:
            a = m; continue
        if abs(fm) < eps:
            return m
        if fa*fm <= 0:
            b = m; fb = fm
        else:
            a = m; fa = fm
    return 0.5*(a+b)



def mkdirectory(path):    
     """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
text_l=['a','b']
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))  
for i0 in range(2):    
    ax = axes[i0]
    if i0 == 0:   
        n_l =[100,200,300,400,500,600,700,800,900,1000] 
        L = []  # x-axis：L
        pc_std = []  # y-axis：σ(p_c)

        for n in n_l:  
            dic_sim_pc = {}  # sim:pc
            sim_pc_list = []
            for network_id in range(100): 
                folder_path = 'deal_result/L'+str(n)+'/zeta='+str(n)+'/NetID='+str(network_id)  
                if os.path.exists(folder_path) and os.path.isdir(folder_path): 
                    print(n)
                    if network_id == 0:
                        max_sim = 0
                    f_pc = open(folder_path+'/sim_p_pc.txt','r',encoding='utf-8-sig')
                    for i in f_pc:
                        i = i.strip().split('\t')
                        dic_sim_pc[max_sim+int(i[0][3:])] = float(i[1][1:])
                        sim_pc_list.append(float(i[1][1:]))
                    f_pc.close()
                    
                    
                else:
                    break
                max_sim = max(dic_sim_pc)+1  
            pc_std.append(np.std(sim_pc_list))
       
        L0 = np.array(n_l)
        P_STD = np.array(pc_std)
        x =-1

        P_STD_theory =  0.25*((L0+0.0) ** x)

        ax.plot(L0, P_STD_theory, ls='-', lw=2, color='#D7592C', alpha = 1,label=r'slope=-1')
        ax.scatter(L0, P_STD, facecolors='none',edgecolors='#D7592C',s=220)
       
      
        
        ax.set_xlabel(r' $L$', fontsize=30)
        ax.set_ylabel(r'σ($p_c$)', fontsize=30)
        ax.legend(frameon=False,fontsize=13.6)
    
    if i0 == 1:   
        n_l =[100,200,300,400,500,600,700,800,900,1000] 

        L = []  # x-axis：L
        pc_ave = []  # y-axis：<pc(L) - pc(∞)>，pc(∞) represents the theoretical value in the ER network.

        # Calculate pc(∞), <k> = 10,T=6
        if intervals:
            a,b = intervals[0]
            S_c = refine(a,b)
            pc_inf = p_from_S_by_derivative(S_c)
            # pc_inf = 0.24208327778824767
        else:
            print("No root interval found; try different scan resolution.")

        for n in n_l: 
            print(n)
            dic_sim_pc = {} 
            sim_pc_list = []
            for network_id in range(100): 
                folder_path = 'deal_result/L'+str(n)+'/zeta='+str(n)+'/NetID='+str(network_id)  
                if os.path.exists(folder_path) and os.path.isdir(folder_path): 
                    if network_id == 0:
                        max_sim = 0
                    f_pc = open(folder_path+'/sim_p_pc.txt','r',encoding='utf-8-sig')
                    for i in f_pc:
                        i = i.strip().split('\t')
                        dic_sim_pc[max_sim+int(i[0][3:])] = float(i[1][1:])
                        sim_pc_list.append(abs(float(i[1][1:])-pc_inf))
                    f_pc.close()
                    
                else:
                    break
                max_sim = max(dic_sim_pc)+1  
            pc_ave.append(sum(sim_pc_list)/len(sim_pc_list))
            
       
        L0 = np.array(n_l)
        P_STD = np.array(pc_ave)

        

        x =-4/3
        P_STD_theory =  1.7*((L0+0.0) ** x)
        ax.plot(L0, P_STD_theory, ls='-', lw=2, color='#D7592C', alpha = 1,label=r'slope=-4/3')
        ax.scatter(L0, P_STD, facecolors='none',edgecolors='#D7592C',s=220)
       
        ax.set_xlabel(r' $L$', fontsize=30)
        ax.set_ylabel(r'$\langle p_c(L)-p_c(\infty) \rangle$', fontsize=30)

    ax.set_xscale('log')
    ax.set_yscale('log')
    
    
    ax.tick_params(axis='x', labelsize=28)
    ax.tick_params(axis='y', labelsize=28)
    ax.text(-0.01, 1.15, text_l[i0], 
          transform=ax.transAxes,  
          fontsize=60,  
          # fontweight='bold',    
          fontfamily='SimHei',    
          ha='left', va='top')        
    
    
    ax.legend(frameon=False,fontsize=18)
   
    ax.set_title('ζ=L', fontsize=25)
    

plt.savefig('figS5.pdf')
plt.tight_layout()
plt.show()






   



   
