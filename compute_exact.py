# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:23:40 2016

@author: tofunth
"""

from utils import load_graph, convert_undirected, save_statistics
import os
from question1 import statistics
# %% prepare the data
data = [
    'wiki-Vote.txt', 'soc-Epinions1.txt','gplus_combined.txt', 
    'soc-pokec-relationships.txt', 'soc-LiveJournal1.txt'
    ]

prefix = '../data'
res_prefix = '../results'
# %% load the data as directed graphs and compute the statistics
for filename in data:
    print 'processing '+filename+'...'
    # compute directed version
    G = load_graph(filename, prefix, directed=True)
    nodes, edges, mean, median, diameter, eff_diameter = statistics(G)
    # save the data
    filen, fileext = os.path.splitext(filename)
    res_filename = filen+'-directed'+fileext
    save_statistics(res_filename, res_prefix, mean, median, diameter, eff_diameter)
    print 'computing exact stats for '+filename+' (directed) completes!'
    # compute undirected version
    G_u = convert_undirected(G)
    nodes_u, edges_u, mean_u, median_u, diameter_u, eff_diameter_u= statistics(G_u)
    res_filename = filen+'-undirected'+fileext
    save_statistics(res_filename, res_prefix, mean_u, median_u, diameter_u, eff_diameter_u)