import utils
import sys
import random
from pyvis.network import Network

def main():
	# call your functions here.

	return # done with main()

## write your functions here.
def read_edges(infile):
	nodes = []
	edgelist = []
	adjlist = {}

	# WRITE CODE HERE
	
	return nodes,edgelist,adjlist

## INSTRUCTIONS: you must comment what EACH LINE DOES in this
## function. Print statements are your friend here. 
## Note that you should complete the read_edges() function
## before working on this. 
def single_edge_betweenness(nodes,paths,u,v):
	between = 0
	for i in range(len(nodes)):
		s = nodes[i]
		for j in range(i+1,len(nodes)):
			t = nodes[j]
			if len(paths[s][t]) != 0:
				num_on_path = 0
				for path in paths[s][t]:
					for n in range(len(path)-1):
						if (path[n] == u and path[n+1] == v) or (path[n] == v and path[n+1] == u):
							num_on_path+=1
				between += num_on_path / len(paths[s][t])
	return between

def edge_betweenness(nodes, edges, paths):
	B = {}
	
	# WRITE CODE HERE

	return B

def GN(nodes,edgelist,adjlist):
	partitions = [[nodes]]

	# WRITE CODE HERE
	
	return partitions

# keep this at the bottom of the file.
if __name__ == '__main__':
	main()

