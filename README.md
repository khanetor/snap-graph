Snap Graphs
===========

### Installation
1. Use Python 2.7!
2. Download the graphs from [here](http://snap.stanford.edu/data/index.html).
3. Download ```SNAP.py``` from [here](http://snap.stanford.edu/snappy/release).
4. Install SNAP.py with
   * Install into python path
	 ```sh
	 tar zxvf snap-3.0.0-3.0-[platform]-x64-py2.7.tar.gz
	 cd snap-3.0.0-3.0-[platform]-x64-py2.7
	 sudo python setup.py install
	 ```
   * Or you can simply copy ```_snap.so``` and ```snap.py``` to your project directory

### Quickstart

The main script to perform statistics computation is ```computer_stats.py```. The script automatically finding the largest strongly connected component if the graph is directed and the largest weakly connected component of the graph is undirected. The methods are performed on this component.

For example, to compute the approximate statistics of the graph wiki-Vote.txt
* which is located in ../data/ 
* saving the results in ../results/
* using the ANF algorithm (a scheme using Flajolet-Martin algorithm), with options:
* k=16 (number of repetitions for each node)
* r=3 (extra bits for the bitmasks)
* converting the graph into an undirected graph before computing

```python
python2 compute_stats.py -d ../data -s ../results -f wiki-Vote.txt -3 -k 16 -r 3 -u
```

Some main options:

* -f: the graph's filename, which is in form of edge list.
* -u: converting the graph into an undirected graph. Leave out this option means the graph is loaded as a directed graph.
* -m: method to use. 0: exact statistics, 1: sampling random pairs of nodes, 2: sampling random pairs of sources and 3: ANF
* -p: the probability of sampling (for method 1 and method 2)
* -k: the number of repetitions for each node (method 3)
* -r: the number of extra bits for each bitmask, which has the length logN, where N is the number of nodes
* -hm: The distance limit (exclusive) to check for ANF algorithm. E.g. h=5 means checking h=1, 2...4

To see the list of options, you can run

```python
python2 compute_stats.py --help
```

### Graph Statistics computations

We implemented 4 methods to compute the graph statistics:

1. Exact statistics: Located in ```exact.py```. Calling method: ```get_exact_statistics(lcc)```
2. Sampling random pairs of nodes: Located in ```sample_pair.py```. Calling method: ```get_sample_pair_statistics(lcc, p)```
3. Sampling random sources and performing BFS: Located in ```sample_source.py```. Calling method: ```get_sample_source_statistics(lcc, p)```
4. ANF algorithm (a scheme of Flajolet-Marting algorithm): Located in ```anf.py```. Calling method: ```get_anf_statistics(lcc, k, r, h_max)```


### Graphs to examine
- wiki-Vote : 7,115 nodes
- soc-Epinions1 : 75,879 nodes
- ego-Gplus : 107,614
- nodes soc-Pokec : 1,632,803 nodes
- soc-LiveJournal1 : 4,847,571 nodes
