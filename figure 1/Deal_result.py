# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import numpy as np
from multiprocessing import Pool 
import matplotlib.pyplot as plt


def mkdirectory(path):    
     """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        

def Deal_R(args):  
    """
    Parses raw simulation logs to extract spatio-temporal activation data.
    
    This function processes the state of each node across realizations, 
    calculates the total active count, and maps nodes to their specific 
    activation time steps.

    Parameters:
        args (tuple)
    """
    i, avg_k, zeta, source_p,T_active,sim_time,resultpath_status,deal_results_time,deal_results_spatial = args
    print('Deal_R for netId:%d, source_p:%f' % (i, source_p))  
    f1 = open(deal_results_time +'active_result.txt','w', encoding='utf-8-sig')
    f2 = open(deal_results_time +'active_result_total.txt','w', encoding='utf-8-sig')
    for simulate_num in range(sim_time): 
        f1.write(str(simulate_num) + '\t')  
        f2.write(str(simulate_num) + '\t')
        sum1 = 0  
        dic_1 = {}  # Map time steps (key) to list of newly activated node coordinates (value)
        f = open(resultpath_status +'sim'+str(simulate_num) + '_status.txt', 'r', encoding='utf-8-sig') 
        for line in f:   
            line = line.strip().split('\t')
            if line[1] == 'active':   
                sum1 += 1  
                if int(line[2]) not in dic_1:   
                    dic_1[int(line[2])] = []    
                dic_1[int(line[2])].append(line[0])   
        f1.write(str(sum1) + '\t')   
        sorted_dic = dict(sorted(dic_1.items()))  
        sorted_dic1 = {}  
        for key, value in sorted_dic.items():
            new_list = []
            for item in value:
                item = item.strip('()')
                num1, num2 = map(int, item.split(','))
                new_list.append((num1, num2))
            sorted_dic1[key] = new_list
        
     
        if len(sorted_dic1) != 0:
        
            max_step = max(sorted_dic1.keys())  
        else:
            max_step = 0
        x_step =  np.arange(max_step+1) 
        y_accumulate = [0  for a in range(max_step+1)]   
        for step in sorted_dic1: 
            f1.write(str(step) + ';')
            y_accumulate[step] += len(sorted_dic1[step]) 
            for z in range(len(sorted_dic1[step])): 
                f2.write(str(sorted_dic1[step][z]) +'\t')
                if z != len(sorted_dic1[step]) - 1:
                    f1.write(str(sorted_dic1[step][z]) +';')
                else:
                    f1.write(str(sorted_dic1[step][z]) +'\t')
        f1.write('\n')
        f2.write('\n')
        f.close()
       
    f1.close()
    f2.close()
    
         
    
    

def Deal_Parallel(i, zeta, avg_k, source_pro,T_active,sim_time):  
    """
    Prepares argument sets for parallel post-processing of simulation results.
    
    This function organizes the output directories for both temporal and spatial 
    analysis and packs them into a list.

    Parameters:
        i (int): Network ID.
        zeta (int): Characteristic link length (spatial parameter).
        avg_k (int): Average degree of the network.
        source_pro (list): List of initial activation fractions (p) analyzed.
        T_active (int): Activation threshold used in simulations.
        sim_time (int): Number of realizations per parameter set.

    """
    args = []  
    resultpath = 'result/'  # Raw simulation data
    deal_resultpath = 'deal_result/'  # Store the processing results
    for source_p in source_pro:
        deal_results_time =  deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/time_result/'
        deal_results_spatial =  deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/spatial_result/' 
        resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/'
        mkdirectory(deal_results_time)  
        mkdirectory(deal_results_spatial)
        args.append([i, avg_k, zeta,source_p,T_active,sim_time,resultpath_status,deal_results_time,deal_results_spatial]) 

    # Create a pool of worker processes for parallel execution
    # The number of processes is set to one-fifth of the length of the source_pro list
    pool = Pool(processes=int(len(source_pro)/5))  
    pool.map(Deal_R, args)  
    pool.close()   
    
       
if __name__ == "__main__":
    # Network Parameters     
    zeta = 3
    avg_k = 10  # Average Degree
    i = 0
    source_pro = [x / 1000 for x in range(1, 1000)]   # The range of initial activation fractions
         
    T_active = 6  # The activation threshold (T)
    sim_time = 20  # Number of independent simulation realizations 
    
    Deal_Parallel(i, zeta, avg_k,source_pro,T_active,sim_time)   
    
    
    
    
