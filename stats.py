# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:38:48 2016

@author: tofunth
"""
import snap


# compute all the statistics
def get_stats(G, directed=True):
    G_LSCC = snap.GetMxScc(G)
    # Find mean, median, diameter, effective diameter
    distance_counter = snap.TIntH()
    
    for n in G_LSCC.Nodes():
        n_id = n.GetId()
        shortest_distances = snap.TIntH()
        snap.GetShortPath(G, n_id, shortest_distances, directed)
    
        for i in shortest_distances:
            if shortest_distances[i] > 0 and distance_counter.IsKey(shortest_distances[i]):
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
    
    i = 0
    half = 0
    while half <= total_distance_count / 2:
        half += distance_counter[distance_counter.GetKey(i)]
        i += 1
    
    # Median
    median = distance_counter.GetKey(i - 1)
    
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
    
    return mean, median, diameter, eff_diameter
    