# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 11:22:53 2025

@author: JialuZhang01
"""

import sys
import os
import random
import numpy as np
import pickle as pk 
import networkx as nx
import itertools as itert
from multiprocessing import Pool 
import matplotlib.pyplot as plt


def mkdirectory(path):     
    """
    Create a directory at the specified path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        
        
def expvariate_sequence(kesi, n, L):
   """
    Generate a sequence of link lengths following an exponential distribution.
    
    Args:
        zeta (int): The characteristic link length.
        n (int): Number of edges (links).
        L (int): Linear system size (number of nodes per row/column).
        
    Returns:
        list: A list containing n generated link lengths.
    """
    sample = []  
    i = 0    
    while i < n:   
        p = random.random()
        x = -kesi*np.log(1-p)
        length = x
        if length <= L/2:  # Apply Periodic Boundary Conditions (PBC)
            sample.append(length)
            i += 1
            
    return sample


def save(ResultPath, results):  
   """
    Serializes and saves the result object to a .pkl file using the pickle module.
    
    Args:
        ResultPath (str): The destination file path.
        results: The data object.
    """
   pk.dump(results, open(ResultPath, "wb"))
   
   
def findCandidateCoordinate(link_length):  
   """
    Identifies the lattice coordinates closest to a circle centered at the origin 
    with a radius equal to the given link_length.
    
    Args:
        link_length (float): The target Euclidean distance for the link.
        
    Returns:
        all_ccoordinates : list
        List of candidate coordinates.
        cc_circle : dict
            Dictionary containing distances from lattice points to the circle.
        cc_lattice : dict
            Dictionary containing distances from lattice points to the other lattice points.
    """
    max_l = np.ceil(link_length)  
    enumerate_length = np.arange(0, max_l, 1)  # [0,1,2,....max_l-1]
    
    # Store distances from lattice points to the circle
    cc_lattice = {}  
    cc_circle = {}  
    
    # Iterate over lattice points
    for deltax in enumerate_length:  # 遍历[0,1,2,....max_l-1]
        deltay = np.sqrt(np.power(link_length,2)-np.power(deltax, 2))  
        lattice_deltax = deltax
        lattice_deltay = round(deltay,0)  
        
        
        cc_circle[(deltax,deltay)] = abs(np.sqrt(lattice_deltax**2+lattice_deltay**2)-link_length)  
        cc_lattice[(lattice_deltax,lattice_deltay)] = abs((lattice_deltay+deltay)*(lattice_deltay-deltay)) #calculate the shortest distance from the point (lattice_deltax, lattice_deltay) to circle
        
   
    s_value_k = {cc_lattice[each]:each for each in cc_lattice.keys()} 
    min_s = min(cc_lattice.values())
    coord_sd = s_value_k[min_s] #coordinate that close to circle with shortset distance     
    
    # Generate all candidate coordinates 
    x = coord_sd[0]
    y = coord_sd[1]
    all_ccoordinates = [(x,y),(-x,y),(x,-y),(-x,-y),(y,x),(-y,x),(y,-x),(-y,-x)] 
    
    return all_ccoordinates, cc_circle, cc_lattice


def CheckPeriodicBoundary(x, y, max_coordinate):  
    '''
    Check if a point (x, y) lies within the periodic boundary conditions.

    Parameters
    ----------
    x : int
        x-coordinate of the point.
    y : int
        y-coordinate of the point.
    max_coordinate : int
        Maximum value for the coordinates.

    Returns
    -------
    x_upd : int
        Updated x-coordinate after considering periodic boundary conditions.
    y_upd : int
        Updated y-coordinate after considering periodic boundary conditions.
    '''
    x_upd = x 
    y_upd = y  
    L = max_coordinate+1
    
    if x > max_coordinate:  
        x_upd = x%L   
    if y > max_coordinate: 
        y_upd = y%L  
    if x < 0:   
        x_upd = (x+L)%L    
    if y < 0:   
        y_upd = (y+L)%L
    
    return x_upd, y_upd 


def CheckNeighbors(G, source_node, nodex, nodey, cc_shortest, max_coordinate): 
    '''

    Returns
    -------
    nodex : int
        Updated x-coordinate of the node.
    nodey : int
        Updated y-coordinate of the node.
    state : bool
        Boolean indicating if there are effective candidate nodes.

    '''
    count = 0
    state = True #judge whether there is a effective candidate 
    
    # Check if the current node is a neighbor of the source node
    while (nodex,nodey) in list(G.neighbors(source_node)):
        # Reassign select the candidate
        candidate_coord =  random.choice(cc_shortest) #random selects a candidate
        #get a new assigned node
        assigned_node_x = source_node[0]+candidate_coord[0]
        assigned_node_y = source_node[1]+candidate_coord[1]
        # Judge or update the coordinate 
        [nodex, nodey]= CheckPeriodicBoundary(assigned_node_x, assigned_node_y,max_coordinate)
        count += 1
        # If count exceeds the number of candidate coordinates, set state to False and break loop
        if count > len(cc_shortest):
            state = False
            break
        
    return nodex, nodey, state
   
   
def NetworkCreate(range_coordinate, links, networkpath, filename): 
   '''
    Create a spatial network with given range of coordinates and links.

    Parameters
    ----------
    range_coordinate : list
        Range of coordinates for the network.
    links : list
        List of link lengths.
    networkpath : str
        Path to save the network file.
    filename : str
        Name of the network file.

    Returns
    -------
    G : graph
        The generated spatial network.

    '''
    G = nx.Graph()   # Create the empty graph    
    max_coordinate = max(range_coordinate)  # calculate the maximum coordinates
    for coordinate in itert.product(range_coordinate,range_coordinate):  # Generate the nodes with coordinates and add the nodes
        G.add_node(coordinate) 
        
    # Add the edges
    # Assign the links to nodes
    state = True
    nodes = list(G.nodes())  
    link_num = 0  
    while link_num < len(links):  
        link_length = links[link_num]   #obatin the length of links
        source_node = random.choice(nodes)  # randomly select a source node and find a candiate coordinate base
        [cc_shortest,cc_circle,cc_lattice]  = findCandidateCoordinate(link_length)
        cc_shortest_set= list(set(cc_shortest))  
        
        # If link_length < 0.5, change (0,0) to [(0,1), (0,-1), (1,0), (-1,0)]
        if cc_shortest_set[0] == (0,0):
            cc_shortest_set = [(0,1),(0,-1),(1,0),(-1,0)]  
        candidate_coord = random.choice(cc_shortest_set)  # Randomly select a candidate node   
        # Get a new assigned node
        assigned_node_x = source_node[0]+candidate_coord[0]  
        assigned_node_y = source_node[1]+candidate_coord[1] 
             
        [nodex, nodey]= CheckPeriodicBoundary(assigned_node_x, assigned_node_y, max_coordinate)  # Update the coordinate  

        # Judge whether new node is in the neighbor of source node to avoid multiple edges between two nodes
        if (nodex,nodey) in list(G.neighbors(source_node)): 
            [nodex, nodey, state] = CheckNeighbors(G, source_node, nodex, nodey, cc_shortest_set, max_coordinate)
        
        #  Successfully add the link into the network if state == True
        if state  == True:  
            G.add_edge(source_node,(nodex,nodey))  
            link_num += 1  
            print('%d links have been added'%link_num)
        else:   # if state == False,change the source node 
            continue 
        
    # Examine whether the network has been created successfully
    if link_num == len(links):  
        print('network has been created successfully')
        save(networkpath+'/'+filename + '_spatialNet.pkl', G)  
    else:
        print('failed to create')
    
    return G   


def GenerateZetaNet(args):  
   """
    Generate network for specific parameters

    Args:
        args (list): List of parameters including network ID (i), average degree (avg_k),
                     zeta value (zeta), number of edges (M), lattice length (L), and network save path (networkpath)

    Returns:
        None
    """
    i, avg_k, zeta, M, L, networkpath = args
    range_coordinate = np.arange(0, L, 1)  #  # Coordinate range[0,1,2,...,999] (L = 1000)
    # Generate sequence of links with specified length and parameters   
    print('Generating network for netId:%d, zeta:%d' % (i, zeta))  
           
    links = expvariate_sequence(zeta, M, L)  
    networkpath_link = os.path.join(networkpath, f'NetID{i}_avgk{avg_k}_links_zeta{zeta}.pkl')  # sequence of link lengths：'network/NetID*_avgk*_links_zeta*.pkl'
    save(networkpath_link, links)  
 
    # Create network 
    filename = f'NetID{i}_avgk{avg_k}_zeta{zeta}'  # NetID*_avgk*_zeta*.*
    NetworkCreate(range_coordinate, links, networkpath, filename)
       
    
    

def GNParallel(networkpath, i, zetas, avg_k, M, L): 
    '''
        Generate networks in parallel.

    Parameters
    ----------
    networkpath : str
             Path to save the networks.
    i : int
        Network ID.
    zetas : list
        List of zeta values.
    avg_k : int
        Average degree.
    M : int
        Number of edges.
    L : int
        Lattice length.

    Returns
    -------
    None.
    '''
   
    args = []  
    for zeta in zetas:
        args.append([i, avg_k, zeta, M, L, networkpath])   
    
    # Create a pool of worker processes for parallel execution
    # The number of processes is set to one-fifth of the length of the zetas list
    # This ensures efficient utilization of system resources while parallelizing the network generation process
    pool = Pool(processes=int(len(zetas)/5))  
    pool.map(GenerateZetaNet, args) 
    pool.close()  
    
       
if __name__ == "__main__":
    networkpath = 'network/'  
    mkdirectory(networkpath)  # Create folder to save networks
    #  Create network  
    L = 1000    # Lattice length
    N = L * L  # Number of nodes
    # Define range of zeta values:[3,4,5,...19,20,30,40,50,...,90,100,500,1000]
    zetas = list(np.arange(3, 21)) + [30, 40,50, 60, 70, 80, 90, 100, 500, 1000]
    avg_k = 10   # Set Average Degree
    i = 0
    
    print('Begin to generate the network...') 
    M = int((N * avg_k) / 2)  # Calculate number of edges
    GNParallel(networkpath, i, zetas, avg_k, M, L)   # Parallel Generation Network
    print('Finish generating the network.')    
    
    
    
