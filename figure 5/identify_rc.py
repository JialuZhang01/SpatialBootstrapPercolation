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
        add_active = []   # store nodes that will flip to 'active' in this time step
        inactive_nodes = list(set(l_nodes)-set(list_active))  # Identify nodes that are currently inactive
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
    
    
def Local_Percolation(G,i, avg_k, zeta,source_i,T_active,sim_t, max_steps,resultpath_status,selected_sets_l,dic_status_random,L_nodes):
    """
    A realization of the percolation process.
  
    Parameters:
        G (networkx.Graph): The spatial network (zeta-model).
        i, avg_k, zeta: Network parameters (index, average degree, link length).
        source_i: Index for the pre-selected initial seed set.
        T_active (int): Activation threshold (T).
        sim_t (int): The current realization index.
        max_steps (int): Maximum time steps for each cascade.
        resultpath_status: Output paths for saving.
        selected_sets_l (list): Pre-generated initial seed nodes for all simulations.
        dic_status_random (dict): random background.
        L_nodes (list): List of all nodes.

    Returns:
        dict: The state dictionary of the final simulation realization.
    """
    List_source = selected_sets_l[0][source_i] 
    Dic_status_original = {} 
    for node in G.nodes(): 
        Dic_status_original[node] = ['inactive',-1]
    Dic_status_l = copy.deepcopy(Dic_status_original)  
    
    List_active = []  
    for source_positive in List_source:  
        if dic_status_random[source_positive][0]  != 'active':
            Dic_status_l[source_positive] = ['active', 0] 
            List_active.append(source_positive)  
    for i_r in dic_status_random:
        if dic_status_random[i_r][0] == 'active':
            Dic_status_l[i_r] = ['active', 0]  
            List_active.append(i_r) 
       
    dic_status_local = percolation_course(G,List_active,Dic_status_l,T_active,max_steps,L_nodes) 
    save_results(resultpath_status, sim_t,dic_status_local) 
    return dic_status_local
    

 

def BP_deal_pfinal(sim_r,G, i, avg_k,zeta,T_active,sim_t,max_steps,selected_sets_l,dic_status_random,L_nodes): 
    """
    Executes a local percolation simulation and computes the final p_infinity.
    
   
    Parameters:
        sim_radius (int): The radius parameter for the initial seed set.
        G (networkx.Graph): Underlying spatial network.
        i, avg_k, zeta: Network parameters (index, average degree, link length).
        T_active (int): Activation threshold (T).
        sim_t (int): Current realization index.
        max_steps (int): Maximum time steps for each cascade.
        selected_sets_l (list): Pre-generated initial seed nodes for all simulations.
        dic_status_random (dict): random background.
        L_nodes (list): List of all nodes.

    Returns:
        float: The LCC at the steady state.
    """
    resultpath = 'result/'  
    print('Local_Percolation for avg_k:%f, source_r:%d' % (avg_k, sim_r)) 
    resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source_r{sim_r}_T{T_active}'+ '/'  
    source_i = radius_list.index(sim_r)  
    mkdirectory(resultpath_status) 
    Dic_status_local = Local_Percolation(G,i, avg_k, zeta,source_i,T_active,sim_t, max_steps,resultpath_status,selected_sets_l,dic_status_random,L_nodes)  
    p_infin_local = Get_P_infinite(Dic_status_local)
    
    
    return p_infin_local
    
  

def now_find_rc(radius_l,G,i, avg_k,zeta,T_active,simulation,max_steps,L_nodes,dic_status_random,selected_sets_l): 
    """
    Identifies the critical nucleation radius (Rc) using a binary search algorithm.
    Rc is defined as the minimum seed radius required to trigger a global cascade 


    Parameters:
        radius_l (list): Sorted list of candidate seed radii [R1, R2, ...].
        G (networkx.Graph): The spatial network.
        i, avg_k, zeta: Network parameters (index, average degree, link length).
        simulation (int): Number of independent realizations.
        max_steps (int): Maximum time steps for each cascade.
        L_nodes (list): List of all nodes.
        dic_status_random(dict)：The status of nodes.
        selected_sets_l (list): Pre-generated initial seed nodes for all simulations.
        

    Returns:
        p_rc: The smallest radius in radius_list that leads to global activation.
        dic_r_p(dict): Dictionary tracking the results.
    """
    dic_r_p = {}
    left, right = 0, len(radius_l) - 1  
    rc_index = -1  

    while left <= right: 
        mid = (left + right) // 2 
       
        p_infinite = BP_deal_pfinal(radius_l[mid],G, i, zeta, avg_k,T_active,simulation,max_steps,selected_sets_l,dic_status_random,L_nodes)  
        dic_r_p[radius_l[mid]] = p_infinite
        if p_infinite >= 0.9:  
            rc_index = mid
            right = mid - 1  
        else:  
            left = mid + 1 
            
    p_rc = radius_l[rc_index]
        
    return p_rc,dic_r_p  
   

def points_in_circle(l_nodes, radius_list, l_size,sim0):
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
    
    sim_selected_local = {}
    for sim_t1 in range(sim0):
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
        sim_selected_local[sim_t1]=point_sim
    return sim_selected_local


def Select_nodes(n,l_nodes,source_pro,sim_t):
     """
    Generates nested sets of initial seed nodes for multiple simulation realizations.
    
    This function ensures that for increasing activation fractions (p), the 
    corresponding node sets are strictly increasing subsets.
    
    Parameters:
        n (int): Total number of nodes in the network.
        l_nodes (list): List of all nodes.
        source_pro (list): Sorted list of initial activation fractions (p).
        sim_t (int): Number of independent simulation realizations.
        
    Returns:
        dict: A dictionary where each key is a realization ID and the value is a 
              list of nested node sets corresponding to source_pro.
    """
    sim_selected_p = {}
    for sim_t1_p in range(sim_t):
        node_counts = [max(0, int(p * n)) for p in source_pro]  
        for i0 in range(1, len(node_counts)):  
            if node_counts[i0] <= node_counts[i0-1]:
                node_counts[i0] = node_counts[i0-1] + 1
                
        selected_sets = []
        previous_nodes = set()
                
        for count in node_counts:
            nodes_to_add = count - len(previous_nodes)  
            if nodes_to_add > 0:  
                available_nodes = [a_n for a_n in l_nodes if a_n not in previous_nodes] 
                new_nodes = random.sample(available_nodes, nodes_to_add)
                current_nodes = previous_nodes.union(new_nodes)
            else:
                current_nodes = previous_nodes.copy()
                
            selected_sets.append(current_nodes) 
            previous_nodes = current_nodes 
        sim_selected_p[sim_t1_p]=selected_sets
    
    return sim_selected_p


def Get_P_infinite(dic_status_cal):
    """
    Computes the size of the Giant Connected Component (GCC) as the order parameter P_inf.
    
    This function filters for active nodes, constructs the active subgraph, 
    and identifies the largest cluster to determine the extent of the cascade.

    Parameters:
        dic_status_cal (dict): Status of each node {'node_id': ['active/inactive', time]}.
       
    Returns:
        float: The normalized size of the largest connected component (P_infinity).
    """
    list_active_cal =[]   
    for i_cal in dic_status_cal:
        if dic_status_cal[i_cal][0] == 'active':
            list_active_cal.append(i_cal)
    G1_random = nx.subgraph(G, list_active_cal)
    components = list(nx.connected_components(G1_random)) 
    if len(components) == 0 :
        p_inf = 0
    else:
        largest_component = max(components, key=len) 
        p_inf = int(len(largest_component))/1000000
    return p_inf
    
        
    

def find_rc(zeta,source_p,source_p_list,avg_k,T_active,G,i,sim_time,Selected_sets_p,L_nodes,radius_list,L):
    """
    Evaluates the critical nucleation radius Rc for a given initial density p.
    
    The function follows a hierarchical logic:
    1. Simulates pure random percolation at density p.
    2. If global percolation (P_inf > 0.9) occurs, Rc is defined as 0.
    3. If not, it iteratively searches for the smallest circular seed radius (Rc) 
       required to bridge the gap and trigger a global cascade.
    """
    p_rc_l = []
    random_p_infinite_list = []
    
    print('Random-Percolation for zeta:%d, source_p:%f' % (zeta, source_p))   
    source_i = source_p_list.index(source_p) 
    Dic_status_original = {} 
    for node in G.nodes():  
        Dic_status_original[node] = ['inactive',-1]
    
    for simulation in range(sim_time): 
        Dic_status = copy.deepcopy(Dic_status_original)  
        List_source = Selected_sets_p[simulation][source_i] 
        List_active = []  
        for source_positive in List_source:  
            Dic_status[source_positive] = ['active', 0] 
            List_active.append(source_positive) 
        Dic_status_random = percolation_course(G,List_active,Dic_status,T_active,max_steps,L_nodes) 
        random_p_infinite=Get_P_infinite(Dic_status_random)
        random_p_infinite_list.append(random_p_infinite)
        
        if random_p_infinite > 0.9:
            
            p_rc_l.append(0)
        else:
            simulation0 = 1 
            Selected_sets_local = points_in_circle(L_nodes, radius_list, L,simulation0)
            P_rc,Dic_r_p = now_find_rc(radius_list,G,i,zeta, avg_k,T_active,simulation,max_steps,L_nodes,Dic_status_random,Selected_sets_local)
            p_rc_l.append(P_rc)
            
            path0 = 'deal_result/LCC_text/zeta'+str(zeta)+'/sim_time='+str(simulation)+'/' 
            mkdirectory(path0) 
            f_w = open(path0+'T='+str(T_active) +'_p='+str(source_p) +'_max_connexted.txt','a+', encoding='utf-8-sig')
            for r_sim in Dic_r_p: 
                f_w.write('zeta'+ str(zeta)+'\t'+'r'+str(r_sim) + '\t'+ str(Dic_r_p[r_sim])+'\n')
                     
            f_w.close()
            
            
    return p_rc_l,random_p_infinite_list
        
        
if __name__ == "__main__":
    networkpath = 'network/'   
    # Network Parameters
    L = 1000   # Lattice length
    N = L * L   # Number of nodes
    T_active = 6  # The activation threshold (T)
    sim_time = 1  # Number of independent simulation realizations
    
    zeta = 12  
    avg_k  = 10 # <k>
    source_p_list = [x / 1000 for x in range(85, 266)]   # The range of initial activation fractions
    
    i = 0
    max_r= 501      # The maximum local selection range is set to L/2      

    # Load the pre-generated spatial network from a pickle file
    with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
        G = pk.load(f)  
    L_nodes = []   # The list of all nodes in the network
    for node in G.nodes(): 
        L_nodes.append(node)  
    Selected_sets_p = Select_nodes(N,L_nodes,source_p_list,sim_time)
    max_steps = 5000000   # The global cutoff for the maximum number of cascading iterations
    
    path_write_rc = 'deal_result/source_p_rc/'
    path_write_pinf = 'deal_result/source_p_pinf/'
    mkdirectory(path_write_rc) 
    mkdirectory(path_write_pinf) 
    f_write=open(path_write_rc+'zeta='+str(zeta)+'_p_rc.txt','a+',encoding='utf-8-sig') 
    f_write1=open(path_write_pinf+'zeta='+str(zeta)+'_p_pinf.txt','a+',encoding='utf-8-sig')
    
    for source_p in source_p_list:
        f_write.write('p'+str(source_p)+'\t')  
        f_write1.write('p'+str(source_p)+'\t') 
        print('zeta='+str(zeta)+', source_p:'+str(source_p))

        radius_list = [r_initial for r_initial in range(1,max_r)]  
        p_rc_list,random_p_infinite_l = find_rc(zeta,source_p,source_p_list,avg_k,T_active,G,i,sim_time,Selected_sets_p,L_nodes,radius_list,L)
        
        for random_pinf in range(len(random_p_infinite_l)):  
            if random_pinf!= len(random_p_infinite_l)-1:
                f_write1.write(str(random_p_infinite_l[random_pinf])+ '\t')
            else:
                f_write1.write(str(random_p_infinite_l[random_pinf])+ '\n')
    
    
        for rc in range(len(p_rc_list)):  
            if rc!= len(p_rc_list)-1:
                f_write.write(str(p_rc_list[rc])+ '\t')
            else:
                f_write.write(str(p_rc_list[rc])+ '\n')
                
    f_write.close()
    f_write1.close()
               
           

    
    
    
    
