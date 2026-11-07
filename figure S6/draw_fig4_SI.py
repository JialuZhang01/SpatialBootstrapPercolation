# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: Administor
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit


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



def mkdirectory(path):     # 若文件夹不存在，建立它
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
text_l=['a','b']



fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))  # 1行2列



for i0 in range(2):  # 行索引：0,1,2
   
    ax = axes[i0]
    if i0 == 0:   
        n_l = [100,200,300,400,500,600,700,800,900,1000]
        L = []  # x轴：L
        pc_std = []  # y轴：σ(p_c)
        
        for i_ in n_l:
            f=open('deal_result/pc_std.txt','r',encoding='utf-8-sig')
            for line in f:
                line=line.strip().split(',')
                if int(line[0][1:]) == i_:
                       pc_std.append(float(line[1]))
                       f.close()
                       break

        L0 = np.array(n_l)
        P_STD = np.array(pc_std)
        
       
        def power_func(L, A, alpha):
            return A * L ** alpha

        p_log = np.polyfit(np.log(L0), np.log(P_STD), deg=1)
        alpha_guess, A_guess = p_log[0], np.exp(p_log[1])
        
        # curve_fit
        popt, pcov = curve_fit(power_func, L0, P_STD, p0=[A_guess, alpha_guess])
        A_fit, alpha_fit = popt
        d_A, d_alpha = np.sqrt(np.diag(pcov))
        
        L_fit = np.logspace(np.log10(L0.min()), np.log10(L0.max()), 100)
        P_STD_fit = power_func(L_fit, A_fit, alpha_fit)
        
  
        ax.scatter(L0, P_STD, facecolors='none',edgecolors='#D7592C',s=220)
        ax.plot(L_fit, P_STD_fit, ls='-', lw=2, color='#D7592C', alpha = 1,
                label=rf'slope = {alpha_fit:.3f} $\pm$ {d_alpha:.3f}')
        
        ax.set_xlabel(r' $L$', fontsize=30)
        ax.set_ylabel(r'$\sigma(p_c)$', fontsize=30)
        ax.legend(frameon=False,fontsize=13.6)
        
       
    
    if i0 == 1:   
  
        def power_func(L, A, alpha):
            return A * L ** alpha
        
        n_l =[100,200,300,400,500,600,700,800,900,1000]
        
        L = []  
        pc_ave = []  # y：<pc(L) - pc(∞)>
        
        if intervals:
            a,b = intervals[0]
            S_c = refine(a,b)
            pc_inf = p_from_S_by_derivative(S_c)
        else:
            print("No root interval found; try different scan resolution.")
        
        
        L0 = np.array(n_l)
        for i_ in n_l:
            f=open('deal_result/pc_ave.txt','r',encoding='utf-8-sig')
            for line in f:
                line=line.strip().split(',')
                if int(line[0][1:]) == i_:
                       pc_ave.append(float(line[1]))
                       f.close()
                       break
    
        P_AVE = np.array(pc_ave)
        
        
        p_log = np.polyfit(np.log(L0), np.log(P_AVE), deg=1)
        alpha_guess, A_guess = p_log[0], np.exp(p_log[1])
        
        popt, pcov = curve_fit(power_func, L0, P_AVE, p0=[A_guess, alpha_guess])
        A_fit, alpha_fit = popt
        d_A, d_alpha = np.sqrt(np.diag(pcov))
        L_fit = np.logspace(np.log10(L0.min()), np.log10(L0.max()), 100)
        P_fit = power_func(L_fit, A_fit, alpha_fit)
        ax.scatter(L0, P_AVE, facecolors='none',edgecolors='#D7592C',s=220)    
        ax.plot(L_fit, P_fit, ls='-', lw=2, color='#D7592C', alpha = 1,
                label=rf'slope = {alpha_fit:.3f} $\pm$ {d_alpha:.3f}')
        
        ax.set_xlabel(r' $L$', fontsize=30)
        ax.set_ylabel(r'$\langle p_c(L)-p_c(\infty) \rangle$', fontsize=30)
        ax.legend(frameon=False,fontsize=13.6)
        

    ax.set_xscale('log')
    ax.set_yscale('log')
    
    
    ax.tick_params(axis='x', labelsize=28)
    ax.tick_params(axis='y', labelsize=28)
    ax.text(-0.01, 1.15, text_l[i0], 
          transform=ax.transAxes,  # 基于当前轴的相对坐标（0-1）
          fontsize=60,   # 字号、加粗
          fontfamily='SimHei',     # 关键：设置为黑体（Windows系统）
          ha='left', va='top')            # 左对齐、上对齐，精准贴左上角
    
    
    ax.legend(frameon=False,fontsize=18)
   
    ax.set_title('ζ=L', fontsize=25)
    

path_line = 'SIFIG4/' 
mkdirectory(path_line)
plt.savefig(path_line + 'SI_fig4b.pdf')
plt.tight_layout()
plt.show()






   



   