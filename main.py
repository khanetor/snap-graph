import snap
import question1

G1_dir = snap.LoadEdgeList(snap.PNGraph, 'Wiki-Vote.txt', 0, 1)
nodes, edges, mean, median, diameter, eff_diameter = question1.statistics(G1_dir)

print 'Nodes: %d' % nodes
print 'Edges: %d' % edges
print 'Mean: %f' % mean
print 'Median: %d' % median
print 'Diameter: %d' % diameter
print 'Effective diameter: %d' % eff_diameter

G1_undir = snap.LoadEdgeList(snap.PUNGraph, 'Wiki-Vote.txt', 0, 1)
nodes, edges, mean, median, diameter, eff_diameter = question1.statistics(G1_undir)

print 'Nodes: %d' % nodes
print 'Edges: %d' % edges
print 'Mean: %f' % mean
print 'Median: %d' % median
print 'Diameter: %d' % diameter
print 'Effective diameter: %d' % eff_diameter
