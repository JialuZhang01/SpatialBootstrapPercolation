# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: Administor
"""

import os
import matplotlib.pyplot as plt
import numpy as np



def mkdirectory(path):     
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
text_l=['a','b','c','d']

fig, axes = plt.subplots(
    nrows=1, ncols=2,  
    figsize=(12, 5.5), 
    constrained_layout=True
)





for j0 in range(2):  
    ax = axes[ j0] 

    if  j0 == 0:   
                    
        from scipy.optimize import curve_fit
        
        n_l =[500,600,700,800,900,1000,1500]
        dic_l_info={}
        for n in n_l:
            dic_l_info[n]=[]
        
        f=open('deal_result/nuc_tau.txt','r',encoding='utf-8-sig')
        for line in f:
            line=line.strip().split(',')
            dic_l_info[int(line[0][1:])].append(float(line[1]))
            dic_l_info[int(line[0][1:])].append(float(line[2]))
            
        f.close() 
        noi_l = []
        noi_std_l = []
        for n in n_l:
            noi_l.append(dic_l_info[n][0])
            noi_std_l.append(dic_l_info[n][1])
        
        # numpy
        N = np.array(n_l)
        NOI = np.array(noi_l)
        NOI_std = np.array(noi_std_l)
  
        def power_func(L, A, alpha):
            return A * L ** alpha
 
        popt, pcov = curve_fit(power_func, N, NOI, sigma=NOI_std, absolute_sigma=True)
        A_fit, alpha_fit = popt
        d_A, d_alpha = np.sqrt(np.diag(pcov))
        N_fit = np.logspace(np.log10(N.min()), np.log10(N.max()), 100)
        NOI_fit = power_func(N_fit, A_fit, alpha_fit)

        ax.scatter(N, NOI, facecolors='none',edgecolors='#D7592C',s=220)
        #slope = a ± b
        ax.plot(N_fit, NOI_fit, ls='-', lw=2, color='#D7592C', alpha = 1,
                label=rf'slope = {alpha_fit:.3f} $\pm$ {d_alpha:.3f}')
        
        ax.set_xlabel(r' $L$', fontsize=30)
        ax.set_ylabel(r'$\langle \tau \rangle$', fontsize=30)
        ax.legend(frameon=False,fontsize=14)
   
        
        
    if  j0 == 1:   
        n_l =[100,200,300,400,500,600,700,800,900,1000,1500] 
        noi_l = []
        noi_std_l = []
        dic_l_info={}
        for n in n_l:
            dic_l_info[n]=[]
        f=open('deal_result/bran_info.txt','r',encoding='utf-8-sig')
        for line in f:
            line=line.strip().split(',')
            dic_l_info[int(line[0][1:])].append(float(line[1]))
            dic_l_info[int(line[0][1:])].append(float(line[2]))
            
        f.close() 
        noi_l = []
        noi_std_l = []
        for n in n_l:
            noi_l.append(dic_l_info[n][0])
            noi_std_l.append(dic_l_info[n][1])
        
       
       
        N = np.array(n_l)
        NOI = np.array(noi_l)
        std_NOI= np.array(noi_std_l)
        
        # ----------------------  <τ>  ----------------------
        logN = np.log10(N)
        logNOI = np.log10(NOI)
        p1, cov1 = np.polyfit(logN, logNOI, deg=1, cov=True)
        alpha_tau = p1[0]
        d_alpha_tau = np.sqrt(cov1[0,0])
        A_tau = 10 ** p1[1]
        
        # ----------------------  σ(τ) ----------------------
        logStd = np.log10(std_NOI)
        p2, cov2 = np.polyfit(logN, logStd, deg=1, cov=True)
        alpha_std = p2[0]
        d_alpha_std = np.sqrt(cov2[0,0])
        A_std = 10 ** p2[1]
        N_fit = np.logspace(np.log10(N.min()), np.log10(N.max()), 100)
        NOI_fit = A_tau * (N_fit ** alpha_tau)
        std_fit = A_std * (N_fit ** alpha_std)  
        ax.plot(N_fit, NOI_fit, ls='-', lw=2, color='#D7592C', alpha = 1,
                label=rf'$\langle \tau \rangle$, slope = ${alpha_tau:.3f} \pm {d_alpha_tau:.3f}$')
        ax.plot(N_fit, std_fit, ls='-', lw=2, color='#1072BD', alpha = 1,
                label=rf'$\sigma(\tau)$, slope = ${alpha_std:.3f} \pm {d_alpha_std:.3f}$')
        ax.scatter(N, NOI, facecolors='none',edgecolors='#D7592C',s=220)
        ax.scatter(N, std_NOI, facecolors='none',edgecolors='#1072BD',s=220)
        ax.set_xlabel(r' $L$', fontsize=32)
        ax.set_ylabel(r'$\langle \tau \rangle$', fontsize=32)
       
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    
    ax.tick_params(axis='x', labelsize=28)
    ax.tick_params(axis='y', labelsize=28)
    ax.text(-0.01, 1.15, text_l[j0], 
          transform=ax.transAxes,  #
          fontsize=60,  
          # fontweight='bold',     
          fontfamily='SimHei',     
          ha='left', va='top')           
    
    if j0 == 1:  
        ax.legend(frameon=False,fontsize=12,columnspacing=0.46,ncol=1,loc='upper left')
        
        
    else:
        ax.legend(frameon=False,fontsize=14)
    
    ax.set_title('nucleation process', fontsize=25)
    




path_line = 'FIG4/' 
mkdirectory(path_line)
plt.savefig(path_line + 'fig_4.pdf')
plt.tight_layout()
plt.show()






   



   
