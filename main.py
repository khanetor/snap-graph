from __future__ import division
import snap

G1 = snap.LoadEdgeList(snap.PNGraph, 'Wiki-Vote.txt', 0, 1)
directed = True

G1_LSCC = snap.GetMxScc(G1)
print 'Nodes: %d' % G1_LSCC.GetNodes()
print 'Edges: %d' % G1_LSCC.GetEdges()

# Find mean, median, diameter, effective diameter
distance_counter = snap.TIntH()

for n in G1_LSCC.Nodes():
    n_id = n.GetId()
    shortest_distances = snap.TIntH()
    snap.GetShortPath(G1, n_id, shortest_distances, directed)

    for i in shortest_distances:
        if shortest_distances[i] > 0 and distance_counter.IsKey(shortest_distances[i]):
            distance_counter[shortest_distances[i]] += 1
        else:
            distance_counter[shortest_distances[i]] = 1

# Mean
total_distance = 0
total_path = 0
for i in distance_counter:
    total_distance += i * distance_counter[i]
    total_path += distance_counter[i]

print 'Mean: %f' % (total_distance / total_path)
