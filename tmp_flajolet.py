# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 16:59:36 2016

@author: tofunth
"""

import snap
from utils import load_graph
import numpy as np
# %% generate binary
def get_binary(d):
    for i in range (d):
        rand = np.random.random()
        if rand < 0.5: return 1 << i
    return 1 << i
# %% get the position of the right most zero
def get_pos(b, d):
    for i in range(d):
        if (b & (1<<i)) == 0:
            break
    return i
# %% get average position of right most zero
def get_avg_pos(v, d):
    n = len(v)
    assert n>0
    acc = 0
    for i in range(n):
        acc += get_pos(v[i], d)
    return float(acc)/n
# %% initialize the bitmasks
def initialize_bitmasks(n, k, d):
    M = np.zeros((n, k), dtype=int)
    for i in range(n):
        for j in range(k):
            M[i][j] = get_binary(d)
    return M
# %% bitwise or vector
def bitwiseor (vec1, vec2):
    assert len(vec1) == len(vec2)
    n = len(vec1)
    vec3 = np.zeros((n,), dtype=int)
    for i in range(n):
        vec3[i] = vec1[i] | vec2[i]
    return vec3
# %% compute the statistics
data_dir = '../data'
filename = 'wiki-Vote.txt'

graph = load_graph(filename, data_dir, directed=True)
if isinstance(graph, snap.PNGraph):
    is_directed = True
    lcc = snap.GetMxScc(graph)
    lcc = snap.ConvertGraph(snap.PNGraph, lcc, True)
elif isinstance(graph, snap.PUNGraph):
    is_directed = False
    lcc = snap.GetMxWcc(graph)
    lcc = snap.ConvertGraph(snap.PUNGraph, lcc, True)

    
nodes_n = lcc.GetNodes()
edges_n = lcc.GetEdges()

k = 64
r = 0
d = int(np.ceil(np.log2(nodes_n)))+r
h_max = 20
# initialize the bitmasks for all nodes
Mcur = initialize_bitmasks(nodes_n, k, d)
# distance count
dist_count = np.zeros((h_max+1, 1))
for h in range(1, h_max+1):
    Mlast = np.copy(Mcur)
    # update binary bitmasks
    for e in lcc.Edges():
        src_node = e.GetSrcNId()
        dst_node = e.GetDstNId()
        Mcur[src_node] = bitwiseor(Mcur[src_node], Mlast[dst_node])
    # estimate the count
    acc = 0
    for node in lcc.Nodes():
        i = node.GetId()
        b = get_avg_pos(Mcur[i], d)
        acc += np.power(2.0, b)/.77351     
    dist_count[h] = acc

real_count = np.zeros((h_max+1, 1))
for i in range(1, h_max+1):
    real_count[i] = dist_count[i] - dist_count[i-1]

avg = sum([x*y for x,y in zip(range(h_max+1), real_count)])/sum(real_count)