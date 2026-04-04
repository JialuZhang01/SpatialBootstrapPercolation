# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import os
import random
import numpy as np
import pickle as pk 
from multiprocessing import Pool 
import copy 


def mkdirectory(path):     
     """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
   
   
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
    for i_t in range(1,max_steps):   
        add_active = []   # store nodes that will flip to 'active' in this time step
        inactive_nodes = list(set(l_nodes)-set(list_active))  # Identify nodes that are currently inactive
        
        for inactive_n in inactive_nodes: 
            t_calculate = 0   # Counter for active neighbors
            # Check the status of each neighbor
            for m in g.neighbors(inactive_n):  
                if dic_status[m][0] == 'active':  
                    t_calculate += 1
            if t_calculate >= t_active:  
                add_active.append(inactive_n)
        # Batch update the status and activation time for newly activated nodes
        for a in add_active:
            dic_status[a] = ['active',i_t]    
            list_active.append(a)
        # Convergence check: if no new nodes were activated, the cascade has reached a steady state
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
    
   
def Percolation(args):
    """
    Main driver function for bootstrap percolation simulations.
    
    Parameters:
        args (tuple): A packed tuple containing:
            G (networkx.Graph): The spatial network.
            i, avg_k, zeta: Network parameters (index, average degree, link length).
            source_i: Index for the pre-selected initial seed set.
            T_active (int): Activation threshold (T).
            sim_time (int): Number of independent simulation realizations.
            max_steps (int): Maximum time steps for each cascade.
            networkpath, resultpath_status: IO paths for loading/saving.
            Selected_sets (list): Pre-generated initial seed nodes for all simulations.
            L_nodes (list): List of all nodes.

    Returns:
        dict: The state dictionary of the final simulation realization.
    """
    # Unpack arguments from the tuple
    G,i, avg_k, zeta,source_i,T_active,sim_time,max_steps,networkpath,resultpath_status,Selected_sets,L_nodes = args
    
    Dic_status_original = {}  # Initialize the baseline status for all nodes as 'inactive'
    for node in G.nodes():  # [status (str), activation_time (int)]
        Dic_status_original[node] = ['inactive',-1]
    
    for simulation in range(sim_time): # Iterate through independent simulation realizations
        Dic_status = copy.deepcopy(Dic_status_original)  # Create a fresh copy of the status dictionary for each trial
        List_source = Selected_sets[simulation][source_i]  # Retrieve the initial seed nodes (source) for this specific realization
        List_active = []  # Track nodes currently in the active state

        # Activate initial seed nodes (Time Step 0)
        for source_positive in List_source:  
            Dic_status[source_positive] = ['active', 0] 
            List_active.append(source_positive)  

        # Execute the bootstrap percolation process
        Dic_status = percolation_course(G,List_active,Dic_status,T_active,max_steps,L_nodes) 
        save_results(resultpath_status, simulation,Dic_status) 
    return Dic_status


    

def BPParallel(G,networkpath, i, zeta, avg_k, source_pro,T_active,sim_time,max_steps,Selected_sets,L_nodes): 
    """
    Prepares a list of arguments for parallel bootstrap percolation simulations 
    across different initial activation densities.
    
    Parameters:
        G (networkx.Graph): The spatial network instance.
        networkpath (str): Path to the network data.
        i (int): Network ID or index.
        zeta (int): Characteristic link length.
        avg_k (int): Average degree of the network.
        source_pro (list): A list of initial activation fractions.
        T_active (int): Activation threshold (T).
        sim_time (int): Number of independent realizations.
        max_steps (int): Maximum iteration steps for cascading.
        Selected_sets (list): Pre-determined seed nodes for each realization.
        L_nodes (list): List of all nodes.
        
    """
    
    args = []  
    resultpath = 'result/'  # Folder for storing simulation results
    for source_p in source_pro:
        print('Percolation for netId:%d, source_p:%f' % (i, source_p)) 
        source_i = source_pro.index(source_p) 
        resultpath_status = resultpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/'  # Format: result/NetID..._avgk..._zeta.../source..._T.../
        mkdirectory(resultpath_status)  #  Ensure the output directory exists
        args.append([G,i, avg_k, zeta,source_i,T_active,sim_time, max_steps,networkpath,resultpath_status,Selected_sets,L_nodes]) 

    # Create a pool of worker processes for parallel execution
    # The number of processes is set to one-fifth of the length of the zetas list
    pool = Pool(processes=int(len(source_pro)/5))      
    pool.map(Percolation, args)  
    pool.close()   
    
    
    
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
    
    sim_selected = {}
    for sim_t1 in range(sim_t):
        node_counts = [max(0, int(p * n)) for p in source_pro]  # Calculate the target number of nodes for each fraction p
        # Enforce strict monotonicity to ensure each subsequent set is larger
        for i0 in range(1, len(node_counts)):   
            if node_counts[i0] <= node_counts[i0-1]:
                node_counts[i0] = node_counts[i0-1] + 1
                
        selected_sets = []
        previous_nodes = set()
                
        for count in node_counts:
            nodes_to_add = count - len(previous_nodes)  # Determine how many additional nodes are needed to reach the next count
            if nodes_to_add > 0:   
                available_nodes = [a_n for a_n in l_nodes if a_n not in previous_nodes]  # Select new nodes only from those not already in the seed set
                new_nodes = random.sample(available_nodes, nodes_to_add)
                current_nodes = previous_nodes.union(new_nodes)
            else:
                current_nodes = previous_nodes.copy()
                
            selected_sets.append(current_nodes) 
            previous_nodes = current_nodes 
        sim_selected[sim_t1]=selected_sets

    
    return sim_selected
    
       
if __name__ == "__main__":
    networkpath = 'network/'  
    # Network Parameters
    L = 1000   # Lattice length
    N = L * L # Number of nodes
    
    zetas = list(np.arange(3, 21)) + [30, 40,50, 60, 70, 80, 90, 100, 500, 1000]    # Range of zeta values
    avg_k = 10   # Average Degree
    i = 0
    for zeta in zetas:
         # Load the pre-generated spatial network from a pickle file
         with open(networkpath + f'NetID{i}_avgk{avg_k}_zeta{zeta}_spatialNet.pkl', 'rb') as f:
             G = pk.load(f)  
              
         L_nodes = []    # The list of all nodes in the network
         for node in G.nodes(): 
             L_nodes.append(node)  
         
         # Define the range of initial activation fractions
         # Generates a sequence from 0.001 to 0.999 with a step of 0.001
         source_pro = [x / 1000 for x in range(1, 1000)] 
         
         T_active = 6  # Set the activation threshold (T)
         sim_time = 10  # Number of independent simulation realizations for each parameter set
         Selected_sets = Select_nodes(N,L_nodes,source_pro,sim_time)   # Pre-select nested sets of seed nodes to ensure consistent comparison across p values
         max_steps = 5000000   # Define the global cutoff for the maximum number of cascading iterations
         BPParallel(G,networkpath, i, zeta, avg_k,source_pro,T_active,sim_time,max_steps,Selected_sets,L_nodes)   # Execute the parallel bootstrap percolation simulation




    
    
    
    
