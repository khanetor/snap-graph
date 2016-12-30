# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:23:40 2016

@author: tofunth
"""

from utils import load_graph, save_statistics, get_connected_component
import os
import argparse
from exact import get_exact_statistics
from anf import get_anf_statistics
from sample_source import get_sample_source_statistics
import time


# %% Parse the arguments
parser = argparse.ArgumentParser(description='Compute the exact statistics from the graph')
parser.add_argument('-d', default='../data', help='The directory of the data (default ../data)')
parser.add_argument('-s', default='../results', help='The directory of the results (default ../results)')
parser.add_argument('-f', default=None, help='The filename to compute the graph statistics (default None)')
parser.add_argument('-u', action='store_false', help='Undirected or not (default False)')
parser.add_argument(
    '-m', 
    default=0, 
    help='''Method to compute statistics. 
    0: exact (default), 
    1: sample pairs, 
    2: sample source, 
    3: anf''')
parser.add_argument('-p', default=10, help='Percentage for sampling (default=10%)')
parser.add_argument('-k', default=32, 
                    help='''
                    Number of binary numbers for each node in ANF algorihtm
                    ''')
parser.add_argument('-r', default=0, 
                    help='Extra bit for ANF algorithm (default=0)')
args = parser.parse_args()

data_dir = args.d
results_dir = args.s
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
method = int(args.m)
p = int(args.p)
k = int(args.k)
r = int(args.r)

# %% suffixes for saving files
type_suffix = 'undirected'
if is_directed: type_suffix = 'directed'

method_suffix = 'exact'
params = 'none'
if method==1:
    method_suffix = 'pairs'
    params = 'p'+str(p)
elif method==2:
    method_suffix = 'src'
    params = 'p'+str(p)
elif method==3:
    method_suffix = 'anf'
    params = 'k'+str(k)+'-r'+str(r)


# %% load the data as directed graphs and compute the statistics
for filename in data:
    print 'processing '+filename+'...'
    
    # compute directed version
    print 'graph type: '+type_suffix
    print 'load the graph in '+filename+'...'
    G = load_graph(filename, data_dir, is_directed)
    
    print 'get the largest connected component...'
    lcc = get_connected_component(G)
    
    print 'method: '+method_suffix
    print 'parameters: '+params
    print 'compute the statistics...'
    time0 = time.clock()
    if method == 0: # exact statistics
        nodes, edges, mean, median, diameter, eff_diameter = get_exact_statistics(lcc)
    elif method == 2: # sample source
        nodes, edges, mean, median, diameter, eff_diameter = get_sample_source_statistics(lcc,pct=p)
    elif method == 3: # anf algorithm
        nodes, edges, mean, median, diameter, eff_diameter = get_anf_statistics(lcc,k=k,r=r)
    comp_time = time.clock()-time0
    
    # save the results
    filen, fileext = os.path.splitext(filename)
    # prepare the filename
    res_filename = filen+'-'+type_suffix+'-'+method_suffix+'-'+params+fileext
    save_statistics(
        res_filename, results_dir, 
        nodes, edges, mean, median, diameter, eff_diameter, comp_time)
    print 'The results are saved in '+results_dir+'/'+res_filename