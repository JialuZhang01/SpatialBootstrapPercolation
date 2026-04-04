# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import matplotlib.pyplot as plt
import numpy as np



def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
text_l=['a','b','c','d']
fig, axes = plt.subplots(
    nrows=2, ncols=2,  
    figsize=(12, 11),  
    constrained_layout=True
)



for i0 in range(2):  
    for j0 in range(2):  
        ax = axes[i0, j0] 
    
        if i0 == 0 and j0 == 0:   
            n_l =[500,600,700,800,900,1000,1500]
            noi_l = []
            noi_std_l = []
    
            for n in n_l:  # L
                dic_sim_pc = {}  #  pc2 for each simulation result
                f_pc = open('deal_result/L'+str(n)+'/zeta=12/sim_p_pc.txt','r',encoding='utf-8-sig')
                for i in f_pc:
                    i = i.strip().split('\t')
                    dic_sim_pc[int(i[0][3:])] = float(i[1][1:])
                f_pc.close()
                    
                ave_noi = []  # The corresponding NOI values for each simulation result
                dic_sim_p_noi = {}
                f = open('deal_result/L'+str(n)+'/zeta=12/sim_p_pnoi.txt','r',encoding='utf-8-sig')
               
                for i in f:
                    i = i.strip().split('\t')
                    dic_sim_p_noi[int(i[0][3:])] ={}
                    for j in i[1:]:
                        j = j.strip().split(',')
                        dic_sim_p_noi[int(i[0][3:])][float(j[0])] = int(j[1])
                f.close()
                for sim_t in dic_sim_pc:
                    ave_noi.append(dic_sim_p_noi[sim_t][dic_sim_pc[sim_t]])
                    
             
                noi_l.append(sum(ave_noi)/len(ave_noi))
                noi_std_l.append(np.std(ave_noi))
    
            N = np.array(n_l)
            NOI = np.array(noi_l)
            x =1
    
            NOI_theory =  0.37*(N ** x)
            NOI_std_theory = 0.65*(N ** x)
            ax.plot(N, NOI_theory, ls='-', lw=2, color='#D7592C', alpha = 1,label=r'$\tau$,slope=1')
            ax.scatter(N, NOI, facecolors='none',edgecolors='#D7592C',s=220)
            ax.set_xlabel(r' $L$', fontsize=30)
            ax.set_ylabel(r'$\langle \tau \rangle$', fontsize=30)
            ax.legend(frameon=False,fontsize=13.6)
        
        if i0 == 1 and j0 == 0:   
            zetas = [12,13,14,15,16,17,18,20]
         
            dic_zeta_noi = {}
            dic_zeta_pc = {}
            for z in zetas:
                dic_zeta_noi[z] = []
                dic_zeta_pc[z] ={}
          
            for  z in zetas:
                f=open('deal_result/L1000/zeta='+str(z)+'/sim_p_pc.txt','r',encoding='utf-8-sig')
                for line in f:
                    line=line.strip().split('\t')
                    dic_zeta_pc[z][int(line[0][3:])] = float(line[1][1:])  
                f.close()
                f=open('deal_result/L1000/zeta='+str(z)+'/sim_p_pnoi.txt','r',encoding='utf-8-sig')
                for line in f:
                    line=line.strip().split('\t')
                    for j in line[1:]:
                        j=j.strip().split(',')
                        if float(j[0]) == dic_zeta_pc[z][int(line[0][3:])]:             
                            dic_zeta_noi[z].append(int(j[1])) 
                f.close()
           
            color_list = ['#1072BD', '#77AE43', '#D7592C', '#7F318D']
           
            x = []
            y = []
           
            noi_y_th = []
            for m in dic_zeta_noi:
                x.append(m)
                y.append(sum(dic_zeta_noi[m])/len(dic_zeta_noi[m]))
            
            a = 4200
            for i1 in x:
                noi_y_th.append(a*(i1**(-1)))
    
           
            ax.plot(x, noi_y_th, color=color_list[2], linestyle='-', linewidth=2.2,markersize=8, label='slope=-1')
            ax.scatter(x, y, facecolors='none', edgecolors=color_list[2], marker='o',s=220)
    
            ax.set_xlabel('ζ',fontsize=32)
            ax.set_ylabel(r'$\langle \tau \rangle$', fontsize=32)
            ax.legend(frameon=False,fontsize=13.6)
          
        if i0 == 0 and j0 == 1:   
            n_l =[100,200,300,400,500,600,700,800,900,1000,1500] 
            noi_l = []
            noi_std_l = []
    
            for n in n_l:  # 取每个L下的结果
                print(n)
                dic_sim_pc = {}  
                dic_sim_p_noi = {}
                for network_id in range(100): 
                    folder_path = 'deal_result/L'+str(n)+'/zeta='+str(n)+'/NetID='+str(network_id)  
                    if os.path.exists(folder_path) and os.path.isdir(folder_path):
                        if network_id == 0:
                            max_sim = 0
                        f_pc = open(folder_path+'/sim_p_pc.txt','r',encoding='utf-8-sig')
                        for i in f_pc:
                            i = i.strip().split('\t')
                            dic_sim_pc[max_sim+int(i[0][3:])] = float(i[1][1:])
                        f_pc.close()   
                        ave_noi = [] 
                        f = open(folder_path+'/sim_p_pnoi.txt','r',encoding='utf-8-sig')
                       
                        for i in f:
                            i = i.strip().split('\t')
                            dic_sim_p_noi[max_sim+int(i[0][3:])] ={}
                            for j in i[1:]:
                                j = j.strip().split(',')
                                dic_sim_p_noi[max_sim+int(i[0][3:])][float(j[0])] = int(j[1])
                        f.close()
                        
                    else:
                        break
                    max_sim = max(dic_sim_pc)+1 
                    
                    
                for sim_t in dic_sim_pc:
                    ave_noi.append(dic_sim_p_noi[sim_t][dic_sim_pc[sim_t]])
                noi_l.append(sum(ave_noi)/len(ave_noi))
                noi_std_l.append(np.std(ave_noi))
    
           
            N = np.array(n_l)
            NOI = np.array(noi_l)
            std_NOI= np.array(noi_std_l)
    
            x =2/3
    
            NOI_theory =  3.3*(N ** x)
            NOI_std_theory = 0.65*(N ** x)
            ax.plot(N, NOI_theory, ls='-', lw=2, color='#D7592C', alpha = 1,label=r'$\tau$,slope=2/3')
            ax.plot(N, NOI_std_theory, ls='-', lw=2, color='#1072BD', alpha = 1,label=r'σ($\tau$),slope=2/3')
            ax.scatter(N, NOI, facecolors='none',edgecolors='#D7592C',s=220)
            ax.scatter(N, std_NOI, facecolors='none',edgecolors='#1072BD',s=220)

            ax.set_xlabel(r' $L$', fontsize=32)
            ax.set_ylabel(r'$\langle \tau \rangle$', fontsize=32)
    
        if i0 == 1 and j0 == 1:
            n_l =[100,200,300,400,500,600,700,800,900,1000] 
            c_list = ['#bbbddc','#85b5db','#5485a9','#005272','#b1d245','#799c00','#06884a','#ea5c65','#b32735','#7c0015']
            
            c_index=0
            for n in n_l:  # L
                N =n*n
                pc_p_l = []
                noi_l = []
                
                dic_sim_pc = {}  
                for network_id in range(100): 
                    folder_path = 'deal_result/L'+str(n)+'/zeta='+str(n)+'/NetID='+str(network_id)  
                    if os.path.exists(folder_path) and os.path.isdir(folder_path): 
                        if network_id == 0:
                            max_sim = 0
                        f_pc = open(folder_path+'/p-p_c/sim_p_pnoi.txt','r',encoding='utf-8-sig')
                        for i in f_pc:
                            i = i.strip().split('\t')
                            dic_sim_pc[int(i[0][3:])] ={}
                            pc = float(i[1].strip().split(',')[0]) 
                            pc_NOI = int(i[1].strip().split(',')[1])  
                            for j in i[2:]:
                                j = j.strip().split(',')
                                dic_sim_pc[int(i[0][3:])][round(float(j[0])-pc,4)] =  int(j[1])
                        f_pc.close()
                    else:
                        break
                    max_sim = max(dic_sim_pc)+1  
                 
                
                dic_total_noi = {} 
                for sim_t in dic_sim_pc:
                    for i in dic_sim_pc[sim_t]:
                        if i not in dic_total_noi:
                            dic_total_noi[i] = []
                        dic_total_noi[i].append(dic_sim_pc[sim_t][i])
                for p_cha in dic_total_noi:
                    pc_p_l.append(p_cha*(n**(4/3))) 
                    noi_l.append((sum(dic_total_noi[p_cha])/len(dic_total_noi[p_cha]))/(n**(2/3)))  
                    
                
                Pc_P= np.array(pc_p_l)
                NOI = np.array(noi_l)
   
                ax.scatter(Pc_P, NOI, facecolors='none',edgecolors=c_list[c_index],s=88,label='L='+str(n))
                c_index +=1
                
            x =-1/2   
            NOI_theory = 2.54*(Pc_P ** x) 
            ax.plot(Pc_P, NOI_theory* (Pc_P) ** (0.1) , ls='-', lw=2, color='#310f1b', alpha = 1,label=r'slope=-1/2') 
    
            ax.set_xlabel(r'$(p-p_c)L^{4/3}$', fontsize=32)
            ax.set_ylabel(r'$\frac{\langle \tau \rangle}{L^{2/3}}$', fontsize=32)
            

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.tick_params(axis='x', labelsize=28)
        ax.tick_params(axis='y', labelsize=28)
        ax.text(-0.01, 1.15, text_l[i0*2+j0], 
              transform=ax.transAxes,  
              fontsize=60, 
              # fontweight='bold',    
              fontfamily='SimHei',     
              ha='left', va='top')            
        
        if i0 == 1 and j0 == 1:  
            ax.legend(frameon=False,fontsize=14.5,columnspacing=0.46,ncol=2)
            
        else:
            ax.legend(frameon=False,fontsize=18)
        if j0 == 0:
            ax.set_title('nucleation process', fontsize=25)
        else:
            ax.set_title('branching process', fontsize=25)
        

plt.savefig('fig4/fig4.pdf')
plt.tight_layout()
plt.show()






   



   
