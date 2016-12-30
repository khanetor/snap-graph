# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:23:40 2016

@author: tofunth
"""

from utils import load_graph, convert_undirected, save_statistics
import os
import argparse
from question1 import statistics
import time


# %% Parse the arguments
parser = argparse.ArgumentParser(description='Compute the exact statistics from the graph')
parser.add_argument('-d', default='../data', help='The directory of the data (default ../data)')
parser.add_argument('-r', default='../results', help='The directory of the results (default ../results)')
parser.add_argument('-f', default=None, help='The filename to compute the graph statistics (default None)')
parser.add_argument('-u', action='store_false', help='Undirected or not (default False)')
parser.add_argument(
    '-m',
    action='store_const', 
    const=0, 
    help='''Method to compute statistics. 
    0: exact (default), 
    1: sample pairs, 
    2: sample source, 
    3: anf''')
parser.add_argument('-p', action='store_const', const=10, help='Percentage for sampling (default=10%)')
parser.add_argument('-k', action='store_const', const=32, 
                    help='''
                    Number of binary numbers for each node in ANF algorihtm
                    ''')
parser.add_argument('-r', action='store_coonst', const=0, 
                    help='Extra bit for ANF algorithm (default=0)')
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

is_directed = args.u
method = args.m
p = args.p
k = args.k
r = args.r


# %% suffixes for saving files
type_suffix = 'undirected'
if is_directed: type_suffix = 'directed'

method_suffix = 'exact'
params = ''
if method==1:
    method_suffix = 'pairs'
    params = str(p)
elif method==2:
    method_suffix = 'src'
    params = str(p)
else:
    method_suffix = 'anf'
    params = str(k)+'-'+str(r)



# %% load the data as directed graphs and compute the statistics
for filename in data:
    print 'processing '+filename+'...'
    
    # compute directed version
    G = load_graph(filename, data_dir, directed=True)
    time0 = time.clock()
    nodes, edges, mean, median, diameter, eff_diameter = statistics(G)
    comp_time = time.clock() - time0
    # save the results
    filen, fileext = os.path.splitext(filename)
    res_filename = filen+'-directed'+fileext
    save_statistics(res_filename, results_dir, mean, median, diameter, eff_diameter, comp_time)
    print 'computing exact stats for '+filename+' (directed) completes!'
    
    # compute undirected version
    G_u = convert_undirected(G)
    
    time0 = time.clock()
    nodes_u, edges_u, mean_u, median_u, diameter_u, eff_diameter_u = statistics(G_u)
    comp_time = time.clock() - time0
    # save the results
    res_filename = filen+'-undirected'+fileext
    save_statistics(res_filename, results_dir, mean_u, median_u, diameter_u, eff_diameter_u, comp_time)
    print 'computing exact stats for '+filename+' (undirected) completes!'