from __future__ import division
import snap

G1 = snap.LoadEdgeList(snap.PNGraph, 'Wiki-Vote.txt', 0, 1)
directed = True

G1_LSCC = snap.GetMxScc(G1)
print 'Nodes: %d' % G1_LSCC.GetNodes()
print 'Edges: %d' % G1_LSCC.GetEdges()

# Find mean, median, diameter, effective diameter

total_distance = 0
total_paths = 0

for n in G1_LSCC.Nodes():
    n_id = n.GetId()
    shortest_distances = snap.TIntH()
    snap.GetShortPath(G1, n_id, shortest_distances, directed)

    for i in shortest_distances:
        total_distance += shortest_distances[i]
    total_paths += shortest_distances.Len()

print 'Mean distance: %f' % (total_distance / total_paths)
