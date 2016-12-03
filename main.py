from __future__ import division
import snap
import question1

G1 = snap.LoadEdgeList(snap.PNGraph, 'Wiki-Vote.txt', 0, 1)

nodes, edges, mean, median, diameter, eff_diameter = question1.statistics_directed(G1)

print 'Nodes: %d' % nodes
print 'Edges: %d' % edges
print 'Mean: %f' % mean
print 'Median: %d' % median
print 'Diameter: %d' % diameter
print 'Effective diameter: %d' % eff_diameter
