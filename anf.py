# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 00:01:27 2016

@author: tofunth
"""

from __future__ import division
import snap
import numpy as np


# %% generate a binary number with the length at most d
# only one bit = 1, the probability (bit i = 1) = .5^(i+1)
def get_binary(d):
    for i in range (d):
        rand = np.random.random()
        if rand < 0.5: return 1 << i
    return 1 << i

  
# %% get the position of the first 0 from the right of a binary number b
# b has the length at most d
def get_pos(b, d):
    for i in range(d):
        if (b & (1<<i)) == 0:
            break
    return i


# %% get the average position of the first 0 from the right of a vector v of
# binary numbers
def get_avg_pos(v, d):
    n = len(v)
    assert n>0
    acc = 0
    for i in range(n):
        acc += get_pos(v[i], d)
    return float(acc)/n
    

# %% initialize the bitmasks
# return a matrix size n x k of binary number with the rule of the method get_binary
def initialize_bitmasks(n, k, d):
    M = np.zeros((n, k), dtype=int)
    for i in range(n):
        for j in range(k):
            M[i][j] = get_binary(d)
    return M
    

# %% element-wise bit-wise OR operation on two vectors of binary numbers
def bitwiseor (vec1, vec2):
    assert len(vec1) == len(vec2)
    n = len(vec1)
    vec3 = np.zeros((n,), dtype=int)
    for i in range(n):
        vec3[i] = vec1[i] | vec2[i]
    return vec3
    

def get_statistics(distance_counter):
    n = len(distance_counter)
    total_distance = 0
    total_distance_count = 0
    for i in range(n):
        total_distance += i * distance_counter[i]
        total_distance_count += distance_counter[i]

    # Mean
    mean = total_distance / total_distance_count

    # Median
    i = -1
    half = 0
    half_total_distance_count = total_distance_count / 2
    while half <= half_total_distance_count:
        i += 1
        half += distance_counter[i]

    median = i

    # Diameter
    diameter = n-1

    # Eff Diameter
    i = -1
    eff_quantile = 0
    eff_quantile_distance_count = total_distance_count * 0.9
    while eff_quantile <= eff_quantile_distance_count:
        i += 1
        eff_quantile += distance_counter[i]

    eff_diameter = i
    
    return mean, median, diameter, eff_diameter

# %% main method to compute the approximate statistics using ANF algorithm
def get_anf_statistics(lcc, k=32, r=0, h_max=20):
    nodes_n = lcc.GetNodes() # node size
    edges_n = lcc.GetEdges() # edge size
    
    # the maximum number of digit of binary numbers for Flajolet-Martin algorithm
    d = int(np.ceil(np.log2(nodes_n)))+r 
    
    # initialize the bitmasks for all nodes
    Mcur = initialize_bitmasks(nodes_n, k, d)
    
    # distance count: 
    # dist_count[h] = number of pairs of nodes can be reached with distance h
    dist_count = np.zeros((h_max+1, 1))
    for h in range(1, h_max+1):
        Mlast = np.copy(Mcur)
        
        # update binary bitmasks
        for e in lcc.Edges():
            src_node = e.GetSrcNId()
            dst_node = e.GetDstNId()
            Mcur[src_node] = bitwiseor(Mcur[src_node], Mlast[dst_node])
            
        # estimate the count
        acc = 0 # accumulator
        for node in lcc.Nodes():
            i = node.GetId()
            b = get_avg_pos(Mcur[i], d)
            acc += np.power(2.0, b)/.77351     
        dist_count[h] = acc
        
        if dist_count[h]-dist_count[h-1] == 0:
            break
    
    # min_dist_count[i] = number of pairs of nodes having the shortest distance i
    min_dist_count = [0] * (h)
    for i in range(1, h):
        min_dist_count[i] = int(dist_count[i] - dist_count[i-1])
    
    mean, median, diameter, eff_diameter = get_statistics(min_dist_count)
    
    return nodes_n, edges_n, mean, median, diameter, eff_diameter