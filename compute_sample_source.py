# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 19:01:47 2016

@author: tofunth
"""

from utils import load_graph, convert_undirected, save_statistics
import os
import argparse
import time
from sample_source import sample_source_stats
# %% Parse the arguments
parser = argparse.ArgumentParser(description='Compute the exact statistics from the graph')
parser.add_argument('-d', default='../data', help='The directory of the data (default ../data)')
parser.add_argument('-r', default='../sample_source_results', help='The directory of the results (default ../results)')
parser.add_argument('-f', default=None, help='The filename to compute the graph statistics (default None)')
args = parser.parse_args()

data_dir = args.d
results_dir = args.r
filen = args.f

if filen == None:
    # if filename is not stated, then compute all the files in the default data directory
    data = [
    'wiki-Vote.txt', 'soc-Epinions1.txt','gplus_combined.txt', 
    'soc-pokec-relationships.txt', 'soc-LiveJournal1.txt'
    ]
else:
    data = [filen]
# %% load the data as directed graphs and compute the statistics
for filename in data:
    print 'processing '+filename+'...'
    
    # compute directed version
    G = load_graph(filename, data_dir, directed=True)
    time0 = time.clock()
    nodes, edges, mean, median, diameter, eff_diameter = sample_source_stats(G, .3)
    comp_time = time.clock() - time0
    # save the results
    filen, fileext = os.path.splitext(filename)
    res_filename = filen+'-directed'+fileext
    save_statistics(res_filename, results_dir, mean, median, diameter, eff_diameter, comp_time)
    print 'computing sample source stats for '+filename+' (directed) completes!'
    
    # compute undirected version
    G_u = convert_undirected(G)
    
    time0 = time.clock()
    nodes_u, edges_u, mean_u, median_u, diameter_u, eff_diameter_u = sample_source_stats(G_u, .3)
    comp_time = time.clock() - time0
    # save the results
    res_filename = filen+'-undirected'+fileext
    save_statistics(res_filename, results_dir, mean_u, median_u, diameter_u, eff_diameter_u, comp_time)
    print 'computing sample source stats for '+filename+' (undirected) completes!'