# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 11:56:35 2016

@author: tofunth
"""
import snap
import os

# load the graph from text files
# directed: indicates the graph is directed or not
# prefix: the path of the data
def load_graph(filename, prefix, directed=True):
    # get the path to the file
    filepath = os.path.join(prefix, filename)
    filen, fileext = os.path.splitext(filepath)
    # check whether the file exists and is a text
    assert os.path.isfile(filepath)==True and fileext=='.txt'
    # load the graph from file, the last two params representing src and dest columns
    if directed:
        G = snap.LoadEdgeList(snap.PNGraph, filepath, 0, 1)
    else:
        G = snap.LoadEdgeList(snap.PUNGraph, filepath, 0, 1)
    return G


# convert the graph from directed into undirected
def convert_undirected(G1):
    G2 = snap.ConvertGraph(snap.PUNGraph, G1)
    return G2
    

# get the largest connected component
def get_connected_component(graph):
    if isinstance(graph, snap.PNGraph):
        lcc = snap.GetMxScc(graph)
        # renumber the node numbers from 0 to the size-1
        lcc = snap.ConvertGraph(snap.PNGraph, lcc, True)
    elif isinstance(graph, snap.PUNGraph):
        lcc = snap.GetMxWcc(graph)
        # renumber the node numbers from 0 to the size-1
        lcc = snap.ConvertGraph(snap.PUNGraph, lcc, True)
    else:
        raise NotAGraphError(graph)
    return lcc
    

class NotAGraphError(Exception):
    pass


# save the result to file
def save_statistics(filename, prefix, nodes, edges, med_dist, mean_dist, diam, eff_diam, comp_time):
    # get the path to the file
    filepath = os.path.join(prefix, filename)
    filen, fileext = os.path.splitext(filepath)
    assert fileext=='.txt'
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    with open(filepath, 'w') as f:
        f.write('{} {} {} {} {} {} {}'.format(nodes, edges, med_dist, mean_dist, diam, eff_diam, comp_time))