# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import random
import numpy as np
import pickle as pk 
import copy 
import matplotlib.pyplot as plt
import ast
import networkx as nx



def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path,exist_ok=True)
        

def save(ResultPath, results): 
    """
    Serializes and saves simulation data to a binary file using pickle.

    Parameters:
        result_path (str): The destination file path (typically ends in .pkl or .bin).
        results (object): The Python object to be serialized.
    """
   pk.dump(results, open(ResultPath, "wb"))
   

def percolation_course(g,list_active,dic_status,t_active,max_steps,l_nodes): 
    """
    Execute the iterative bootstrap percolation process on a graph.
    
    Parameters:
        g (networkx.Graph): The underlying network.
        list_active (list): List of currently active nodes.
        dic_status (dict): Dictionary mapping nodes to their status ['active'/'inactive', time_step].
        t_active (int): Activation threshold (T).
        max_steps (int): Maximum number of iterations (time steps) allowed.
        l_nodes (list): List of all nodes.
        
    Returns:
        dict: Updated dic_status containing the final activation state and the time each node flipped.
    """
    for i_step in range(1,max_steps):  
        add_active = []   
        inactive_nodes = list(set(l_nodes)-set(list_active))
        for inactive_n in inactive_nodes: 
            t_calculate = 0  
            for m in g.neighbors(inactive_n):  
                if dic_status[m][0] == 'active':  
                    t_calculate += 1
            if t_calculate >= t_active:  
                add_active.append(inactive_n)
        for a in add_active:
            dic_status[a] = ['active',i_step]    
            list_active.append(a)
        if len(add_active) == 0:   
            break
    
    return dic_status
    

def save_results(resultpath_status,simulate_num,dic_status):
   """
    Exports the status and activation time of each node to a text file.
    
    Parameters:
        resultpath_status (str): Directory path where the results will be saved.
        simulate_num (int): The current simulation realization/index.
        dic_status (dict): Dictionary mapping nodes to [status, activation_time].
    """
    fd = open(resultpath_status + 'sim'+str(simulate_num) + '_status.txt','w') 
    for n in dic_status:
        fd.write(str(n) + '\t'+ str(dic_status[n][0]) + '\t'+ str(dic_status[n][1]) +'\n')
    fd.close()
    


def Percolation(G,i, avg_k, zeta,source_i,T_active,sim_t, max_steps,networkpath,resultpath_status,Selected_sets,L_nodes):
    """
    Main driver function for bootstrap percolation simulations.
    
    Parameters:
            G (networkx.Graph): The spatial network.
            i, avg_k, zeta: Network parameters (index, average degree, link length).
            source_i: Index for the pre-selected initial seed set.
            T_active (int): Activation threshold (T).
            sim_t (int): An independent simulation realizations.
            max_steps (int): Maximum time steps for each cascade.
            networkpath, resultpath_status: IO paths for loading/saving.
            Selected_sets (list): Pre-generated initial seed nodes for all simulations.
            L_nodes (list): List of all nodes.

    """
    Dic_status_original = {} 
    for node in G.nodes(): 
        Dic_status_original[node] = ['inactive',-1]
    
    Dic_status = copy.deepcopy(Dic_status_original) 
    List_source = Selected_sets[sim_t][source_i]
    List_active = []  
    for source_positive in List_source: 
        Dic_status[source_positive] = ['active', 0]  
        List_active.append(source_positive)  
    Dic_status = percolation_course(G,List_active,Dic_status,T_active,max_steps,L_nodes)  
    save_results(resultpath_status, sim_t,Dic_status)  
    


def deal_results(i, zeta, avg_k,sim_r,T_active,sim_t):
    """
    Parses raw simulation logs to extract spatio-temporal activation data.

    Parameters:
        i (int): Network ID.
        zeta (int): Characteristic link length (spatial parameter).
        avg_k (int): Average degree of the network.
        sim_r (int): Radius.
        T_active (int): Activation threshold used in simulations.
        sim_t (int): Number of realizations.

    """
    resultpath = 'result/'  
    deal_resultpath = 'deal_result/time_result/zeta='+str(zeta)+'/sim_time='+str(sim_t)+'/' 
    deal_results_time =  deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/time_result/' 
    resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/' 
    mkdirectory(deal_results_time)  
    
    print('Deal_R for <k>:%f, source_r:%d' % (avg_k, sim_r)) 
    f1 = open(deal_results_time +'active_result.txt','w', encoding='utf-8-sig') 
    f2 = open(deal_results_time +'active_result_total.txt','w', encoding='utf-8-sig')
    
    f1.write(str(sim_t) + '\t')  
    f2.write(str(sim_t) + '\t')  
    sum1 = 0  
    dic_1 = {}   
    f = open(resultpath_status +'sim'+str(sim_t) + '_status.txt', 'r', encoding='utf-8-sig') 
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
    for active_new in range(1,len(y_accumulate)):
        y_accumulate[active_new] += y_accumulate[active_new-1] 
   
    f2.close()
            
    

def find_pfinal(i, zeta, avg_k,sim_r,T_active,sim_t): 
    """
    Computes the size of the Giant Connected Component (GCC).

    Parameters:
        i (int): Network ID.
        zeta (int): Characteristic link length (spatial parameter).
        avg_k (int): Average degree of the network.
        sim_r (int): Radius.
        T_active (int): Activation threshold used in simulations.
        sim_t (int): Number of realizations.
       
    Returns:
        float: The normalized size of the largest connected component (P_infinity).
    """
    deal_resultpath = 'deal_result/time_result/zeta='+str(zeta)+'/sim_time='+str(sim_t)+'/'
    networkpath = 'network/'  
    with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
        G_initial = pk.load(f)  
    dic_r_pfinal = {} 
    print('z='+str(zeta)+', r:'+str(sim_r))
    dic_r_pfinal[sim_r]=[]
 
    f = open(deal_resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/time_result/active_result_total.txt','r',encoding ='utf-8-sig') 
    for line in f:
        G = copy.deepcopy(G_initial)
        list_active =[]   
        line = line.strip().split('\t')
        for j in line[1:]:
            list_active.append(j)
        l_active = [ast.literal_eval(item) for item in list_active]
        G1 = nx.subgraph(G, l_active)
        components = list(nx.connected_components(G1))  
        if len(components) == 0 :
            dic_r_pfinal[sim_r].append(0)
            p_final = 0
        else:
            largest_component = max(components, key=len)  
            p_final = int(len(largest_component))/N
            dic_r_pfinal[sim_r].append(p_final)
    f.close()
    path0 = 'deal_result/LCC_text/zeta'+str(zeta)+'/sim_time='+str(sim_t)+'/' 
    mkdirectory(path0) 
    f_w = open(path0+'T='+str(T_active) +'_avgk='+str(avg_k) +'_max_connexted.txt','a+', encoding='utf-8-sig')
    for i0 in dic_r_pfinal: 
        f_w.write('zeta'+ str(zeta)+'\t'+'r'+str(i0) + '\t')
        for j in range(len(dic_r_pfinal[i0])):
           if j != len(dic_r_pfinal[i0]) -1:
               f_w.write(str(dic_r_pfinal[i0][j])+'\t')
           else:
               f_w.write(str(dic_r_pfinal[i0][j])+'\n')
    f_w.close()
        
    return p_final
    
 
def BP_deal_pfinal(sim_r,G,networkpath, i, zeta, avg_k,T_active,sim_t,max_steps,Selected_sets,L_nodes): 
    """
    Executes a percolation simulation and computes the final p_infinity.
    
    Parameters:
        sim_radius (int): The radius parameter for the initial seed set.
        G (networkx.Graph): Underlying spatial network.
        networkpath: Network Directory
        i, avg_k, zeta: Network parameters (index, average degree, link length).
        T_active (int): Activation threshold (T).
        sim_t (int): Current realization index.
        max_steps (int): Maximum time steps for each cascade.
        selected_Sets (list): Pre-generated initial seed nodes for all simulations.
        L_nodes (list): List of all nodes.

    Returns:
        float: The LCC at the steady state.
    """
    resultpath = 'result/'  
    print('Percolation for avg_k:%f, source_r:%d' % (avg_k, sim_r)) 
    resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/'
    source_i = radius_list.index(sim_r)  # 
    mkdirectory(resultpath_status)  
    Percolation(G,i, avg_k, zeta,source_i,T_active,sim_t, max_steps,networkpath,resultpath_status,Selected_sets,L_nodes)  
    deal_results(i, zeta, avg_k,sim_r,T_active,sim_t) 
    p_infin = find_pfinal(i, zeta, avg_k,sim_r,T_active,sim_t)  
    
    
    return p_infin
    

  

def find_rc(radius_l,G,networkpath, i, zeta, avg_k,T_active,sim_time,max_steps,Selected_sets,L_nodes): 
    """
    Recording $R_c$ across "sim_time" independent realizations for a given $\langle k \rangle$
    """
    k_rc_l = []  
    for sim_t in range(sim_time):  
        left, right = 0, len(radius_l) - 1 
        rc_index = -1  
    
        while left <= right:
            mid = (left + right) // 2  
            
            p_infinite = BP_deal_pfinal(radius_l[mid],G,networkpath, i, zeta, avg_k,T_active,sim_t,max_steps,Selected_sets,L_nodes)  
    
            if p_infinite >= 0.9: 
                rc_index = mid
                right = mid - 1  
            else:   
                left = mid + 1 
                
       
        k_rc_l.append(radius_l[rc_index])
        
    return k_rc_l
   

def points_in_circle(l_nodes, radius_list, l_size,sim_t):
    """
    Generates sets of initial active nodes within circular regions of varying radius.
    
    This function accounts for Periodic Boundary Conditions (PBC), ensuring that 
    circles centered near the grid edges correctly wrap around to the opposite side.

    Parameters:
        L_nodes (list): List of all nodes.
        radius_list (list): Sorted list of radii to generate seeds for.
        l_size (int): # Lattice length
        sim0 (int): Number of independent spatial samples.

    Returns:
        dict: {realization_id: [set_of_nodes_R1, set_of_nodes_R2, ...]}
    """
    sim_selected = {}
    for sim_t1 in range(sim_t):
        index_n = random.randint(0,len(l_nodes)-1)
        center_node = l_nodes[index_n]
        x0, y0 = center_node
        point_sim = []
        for radius in radius_list:
            r2 = radius ** 2
            points = set()
            for x in range(l_size):
                for y in range(l_size):
                    dx = min(abs(x - x0), l_size - abs(x - x0))
                    dy = min(abs(y - y0), l_size - abs(y - y0))
                    if dx * dx + dy * dy <= r2:
                        points.add((x, y))
            point_sim.append(points)
        sim_selected[sim_t1]=point_sim
    return sim_selected

       
if __name__ == "__main__":
    networkpath = 'network/'   #   Network Directory 
  
    L = 500  # Lattice length
    N = L * L  # Number of nodes
    T_active = 6  # The activation threshold (T)
    sim_time = 10  # Number of independent simulation realizations
    
    zeta = 5 
    avg_k_list  = [a_k / 10 for a_k in range(100, 151)] #  List of <k>
    i = 0
    max_r= 251  # The largest range of local selection options
    
    path_write_rc = 'deal_result/avgk_rc/'
    mkdirectory(path_write_rc) 
    f_write=open(path_write_rc+'zeta='+str(zeta)+'_k_rc.txt','a+',encoding='utf-8-sig')
    
    for avg_k in avg_k_list: 
        f_write.write('<k>'+str(avg_k)+'\t') 
        print('zeta='+str(zeta)+', avg_k:'+str(avg_k))
        with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
            G = pk.load(f)  
        L_nodes = []    
        for node in G.nodes():  
            L_nodes.append(node)  
        
        radius_list = [r_initial for r_initial in range(max_r)] 
       
        Selected_sets = points_in_circle(L_nodes, radius_list, L,sim_time)
        max_steps = 5000000 
        k_rc_list=find_rc(radius_list,G,networkpath, i, zeta, avg_k,T_active,sim_time,max_steps,Selected_sets,L_nodes)  
    
        for rc in range(len(k_rc_list)):
            if rc!= len(k_rc_list)-1:
                f_write.write(str(k_rc_list[rc])+ '\t')
            else:
                f_write.write(str(k_rc_list[rc])+ '\n')
    f_write.close()
               
           
        
        
       
    
    

    
    
    
    
