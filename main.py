import snap

G1 = snap.LoadEdgeList(snap.PNGraph, 'Wiki-Vote.txt', 0, 1)

for n in G1.Nodes():
    print n

for e in G1.Edges():
    print e
