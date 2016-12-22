# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:23:40 2016

@author: tofunth
"""

from utils import load_graph, convert_undirected
import snap
from stats import get_stats
# %% prepare the data
prefix = '../data'
filename = 'wiki-Vote.txt'
# %% load the data as directed graphs and compute the statistics
G = load_graph(filename, prefix, directed=True)
print 'Number of edge =', snap.CntUniqDirEdges(G)
(mean, median, diameter) = get_stats(G, directed=True)
#%% converts the graphs to undirected and compute the statistics
G_u = convert_undirected(G)
(mean_u, median_u, diameter_u) = get_stats(G_u, directed=False)