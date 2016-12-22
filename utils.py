# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 11:56:35 2016

@author: tofunth
"""
import snap
from os import path

# load the graph from text files
# directed: indicates the graph is directed or not
# prefix: the path of the data
def load_graph(filename, prefix, directed=True):
    # get the path to the file
    filepath = path.join(prefix, filename)
    filen, fileext = path.splitext(filepath)
    # check whether the file exists and is a text
    assert path.isfile(filepath)==True and fileext=='.txt'
    # load the graph from file, the last two params representing src and dest columns
    G = snap.LoadEdgeList(snap.PNGraph, filepath, 0, 1)
    return G


# convert the graph from directed into undirected
def convert_undirected(G1):
    G2 = snap.ConvertGraph(snap.PUNGraph, G1)
    return G2


# save the result to file
def save_statistics(filename, prefix, med_dist, mean_dist, diam, eff_diam):
    # get the path to the file
    filepath = path.join(prefix, filename)
    filen, fileext = path.splitext(filepath)
    assert fileext=='.txt'
    with open(filepath, 'w') as f:
        f.write('{} {} {} {}'.format(med_dist, mean_dist, diam, eff_diam))