from __future__ import division
import snap
from exception import NotAGraphError, NotValidParameter
from random import randint


# Sample random pairs

def get_sample_pair_statistics(lcc, p):
    if not 1 <= p <= 100:
        raise NotValidParameter('n should be between 1 and 100')
    elif isinstance(lcc, snap.PNGraph):
        is_directed = True
    elif isinstance(lcc, snap.PUNGraph):
        is_directed = False
    else:
        raise NotAGraphError(lcc)

    nodes = lcc.GetNodes()
    edges = lcc.GetEdges()

    # Find mean, median, diameter, effective diameter
    distance_counter = snap.TIntH()
    cc = 0

    for n in lcc.Nodes():
        for m in lcc.Nodes():
            if randint(0, 100) > p:  # a pair of nodes have p percent chance to be chosen
                continue
            else:
                cc += 1
                print '%d / %d' % (cc, nodes**2)
                n_id = n.GetId()
                m_id = m.GetId()
                length = snap.GetShortPath(lcc, n_id, m_id, is_directed)

                if length <= 0:
                    continue
                else:
                    if distance_counter.IsKey(length):
                        distance_counter[length] += 1
                    else:
                        distance_counter[length] = 1

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
