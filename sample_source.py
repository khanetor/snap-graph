# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 16:54:53 2016

@author: tofunth
"""

from __future__ import division
import snap
import numpy as np


def sample_source_stats(graph, pct):
    if isinstance(graph, snap.PNGraph):
        is_directed = True
        lcc = snap.GetMxScc(graph)
    elif isinstance(graph, snap.PUNGraph):
        is_directed = False
        lcc = snap.GetMxWcc(graph)
    else:
        raise NotAGraphError(graph)

    nodes = lcc.GetNodes()
    edges = lcc.GetEdges()

    # Find mean, median, diameter, effective diameter
    distance_counter = snap.TIntH()

    for n in lcc.Nodes():
        ran_num = np.random.random()
        if ran_num < pct:
            n_id = n.GetId()
            shortest_distances = snap.TIntH()
            snap.GetShortPath(lcc, n_id, shortest_distances, is_directed)
    
            for i in shortest_distances:
                if shortest_distances[i] <= 0:
                    continue
    
                if distance_counter.IsKey(shortest_distances[i]):
                    distance_counter[shortest_distances[i]] += 1
                else:
                    distance_counter[shortest_distances[i]] = 1

    total_distance = 0
    total_distance_count = 0
    for i in distance_counter:
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
        half += distance_counter[distance_counter.GetKey(i)]

    median = distance_counter.GetKey(i)

    # Diameter
    diameter = distance_counter.GetKey(distance_counter.Len() - 1)

    # Eff Diameter
    i = -1
    eff_quantile = 0
    eff_quantile_distance_count = total_distance_count * 0.9
    while eff_quantile <= eff_quantile_distance_count:
        i += 1
        eff_quantile += distance_counter[distance_counter.GetKey(i)]

    eff_diameter = distance_counter.GetKey(i)

    return nodes, edges, mean, median, diameter, eff_diameter
    
class NotAGraphError(Exception):
    pass