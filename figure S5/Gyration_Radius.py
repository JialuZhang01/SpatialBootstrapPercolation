# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 15:54:19 2025

@author: JialuZhang01
"""
import os 
import numpy as np
import math
import networkx as nx
import pickle as pk
import copy
import ast



def mkdirectory(path):    
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def gyration_radius(cluster, L):
   """
    Calculates the squared radius of gyration and center of mass for a 2D cluster 
    under Periodic Boundary Conditions (PBC).
    
    Parameters:
        cluster (iterable): Collection of (x, y) tuples representing node coordinates.
        L (int): # Lattice length

    Returns:
        square_gyration_radius:R_g
        (x_cm, y_cm) :center of mass
            
    """
    x_avg_cor1 = x_avg_cor2 = y_avg_cor1 = y_avg_cor2 = 0.0
    # cluster = list(cluster)
    cluster_mass = len(cluster)
    if cluster_mass == 0:
        return 0.0, (0.0, 0.0)

    for x, y in cluster:
        x_avg_cor1 += math.sin((x * math.pi * 2) / L)
        x_avg_cor2 += math.cos((x * math.pi * 2) / L)
        y_avg_cor1 += math.sin((y * math.pi * 2) / L)
        y_avg_cor2 += math.cos((y * math.pi * 2) / L)

    x_avg_cor1 /= cluster_mass
    x_avg_cor2 /= cluster_mass
    y_avg_cor1 /= cluster_mass
    y_avg_cor2 /= cluster_mass

    xcm = L * (math.atan2(-x_avg_cor1, -x_avg_cor2) + math.pi) / (2 * math.pi)
    ycm = L * (math.atan2(-y_avg_cor1, -y_avg_cor2) + math.pi) / (2 * math.pi)

    square_gyration_radius = 0.0
    for x, y in cluster:
        dx = x - xcm
        dy = y - ycm
        if dx > L / 2:
            dx -= L
        elif dx < -L / 2:
            dx += L
        if dy > L / 2:
            dy -= L
        elif dy < -L / 2:
            dy += L
        square_gyration_radius += (dx * dx + dy * dy) / cluster_mass

    return square_gyration_radius, (xcm, ycm)

def build_lattice_graph_coord(L):
    """
    Construct an L x L 2D lattice with periodic boundary conditions (torus).
    Node labels are coordinate tuples: (r, c).
    Returns:
        G: networkx.Graph
    """
    G = nx.Graph()

    for r in range(L):
        for c in range(L):
            u = (r, c)
            # 4 neighbors with periodic wrapping
            neighbors = [
                ((r - 1) % L, c),    
                ((r + 1) % L, c),     
                (r, (c - 1) % L),     
                (r, (c + 1) % L),      
            ]
            for v in neighbors:
                if u < v:              
                    G.add_edge(u, v)

    return G

if __name__ == "__main__":
    networkpath = 'network/'   # 网络文件夹
    # Network Parameters
    L = 1000  # Lattice length
    N = L * L # Number of nodes
    zeta = 12
    avg_k = 10  # <k>
    i = 0  # Network ID
   
    T_active = 6  # The activation threshold (T)
    sim_time = 1 # Number of independent simulation realizations
    G_classsical = build_lattice_graph_coord(L)  # Two-dimensional lattice with periodic boundary conditions
    
    source_p = 0.229  # zeta_pc2
   
    path_read_pinf = 'deal_result/'+ f'NetID{i}_avgk{avg_k}_zeta{zeta}'+'/'+f'source{source_p}_T{T_active}'+ '/time_result/'
    path_write_pinf = 'deal_result_rg/T='+str(T_active)+'/zeta='+str(zeta)+'/'
    mkdirectory(path_write_pinf) 
    
    dic_t_active = {} 
    f_time_active = open(path_read_pinf+'/active_result.txt','r',encoding='utf-8-sig')
    for line in f_time_active:
        line = line.strip().split('\t')
        for step_active in line[2:]:
            s_active = step_active.strip().split(';')
            dic_t_active[int(s_active[0])] = []
            for j in s_active[1:]:
                dic_t_active[int(s_active[0])].append(j)
                
    f_time_active.close()
    for key in dic_t_active:
        dic_t_active[key] = [eval(item) for item in dic_t_active[key]]
    t_max = max(dic_t_active.keys())
        
    for t in range(1, t_max+1):
        dic_t_active[t].extend(dic_t_active[t-1])
    
    for k0 in dic_t_active:
        dic_t_active[k0] = [tuple(int(num) for num in tup) for tup in dic_t_active[k0]]
        
    for t_step in dic_t_active:
        f = open(path_write_pinf+'t_radius.txt','a+',encoding='utf-8-sig')
        f.write('t'+str(t_step)+'\t')
        print('source_p:'+str(source_p)+'_step'+str(t_step))
        G = copy.deepcopy(G_classsical)  
        G1 = nx.subgraph(G, dic_t_active[t_step])
        components = list(nx.connected_components(G1))  
        if len(components) == 0 :
            f.write('0'+'\t'+'0'+'\t'+'0'+'\n')
        else:
            largest_component = max(components, key=len) 
            largest_component0=list(largest_component)
            
            
            cal_radius, (xcm, ycm) = gyration_radius(largest_component0, L)
            f.write(str(cal_radius)+'\t'+str(xcm)+'\t'+str(ycm)+'\n')
        f.close()


