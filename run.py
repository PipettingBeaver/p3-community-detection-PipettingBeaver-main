import utils
import sys
import random
from pyvis.network import Network

def main():
	# call your functions here.
	# read_edges opens file, populates nodes, edgelist, adjlist
	nodes,edgelist,adjlist = read_edges('files/example-edges.txt')
	
	print("Nodes:", nodes)
	print("edgelist: ",edgelist)
	print("adjlist: ",adjlist)

	paths = utils.all_pairs_shortest_paths(adjlist)
	print("paths: ",paths)

	print(single_edge_betweenness(nodes,paths,'v3','v5')) # should be 15.0
	print(single_edge_betweenness(nodes,paths,'v5','v7')) # should be 7.5

	B = edge_betweenness(nodes, edgelist, paths)
	print("B: ",B)
	# paths = edgelist
	#single_edge_betweenness(nodes,paths,u,v)

	return # done with main()

## write your functions here.
def read_edges(infile):
	nodes = []
	edgelist = []
	adjlist = {}

	# Open File and Split/Classify Line Template from P2
	# Walkthrough:
	# Open file, read through each line of the file
	# Split information, assumed to be tuple, example: [1, 2]
	# difference: Feed out information to nodes, edgelist, and adjlist dictionary
	# Instead of just to edgelist

	with open(infile, 'r') as f: # Open file
		for line in f:			 # Read through each line of file
			line = line.strip()  # Remove leading/trailing whitespace, no commas
			parts = line.split()  # Split line into parts, used below

			# Nodes - list,	line = v1  v3 = [v1,v3]
			# look at nodeA and nodeB from [nodeA, nodeB] separately:
			# if they are not in nodes, append it (to avoid duplication)
			if str(parts[0]) not in nodes: nodes.append(str(parts[0]))
			if str(parts[1]) not in nodes: nodes.append(str(parts[1]))

			# Edgelist - list
			edge = (str(parts[0]), str(parts[1]))  # Convert to integers
			edgelist.append(edge)

			# Adjlist - Dictionary
			# We are assuming undirected, so Add B to A, A to B
			# With dictionary, we do not have to worry about duplicate entries
			if str(parts[0]) not in adjlist: adjlist[str(parts[0])] = []
			adjlist[str(parts[0])].append(str(parts[1]))

			if str(parts[1]) not in adjlist: adjlist[str(parts[1])] = []
			adjlist[str(parts[1])].append(str(parts[0]))
	
	return nodes,edgelist,adjlist

## INSTRUCTIONS: you must comment what EACH LINE DOES in this
## function. Print statements are your friend here. 
## Note that you should complete the read_edges() function
## before working on this. 
def single_edge_betweenness(nodes,paths,u,v):
	# This function finds the betweenness value of a single edge.
	# This translates to being the number of shortest paths that occur between the given pair of nodes
	# So are given a nodes list, paths function, and nodes U, V, we will evaluate for each shortest path
	# that contains the edges [U, V] or [V, U] and then increment this edge's betweenness score by 1.

	between = 0 # Set betweenness (# of shortest paths) to 0 to start
	for i in range(len(nodes)): 			# Iterate through all existing nodes, a nested function we duplicate
		s = nodes[i]						# s = our first node. Involved with t to make the dynamic [s, t] edge
		for j in range(i+1,len(nodes)):		# second nested iteration, this is to permutate all node edge combinations
			t = nodes[j]					# t = our second node, involved with s mentioned above.
			if len(paths[s][t]) != 0:		# this conditional is to avoid check when s = t
				num_on_path = 0				# reset the number of times this edge is on any path to 0
				for path in paths[s][t]:			# iterative loop for each shortest path between any given [s, t]  
					for n in range(len(path)-1):	# here, we view path's node list as a range, and iterate through it
													# example: shortest path [A,D] is [A, B, C, D], length of 4. subtract 1 to get 3
													# n will go through through 0 to 3, or all corresponding nodes numerically [0,1,2,3]
						if (path[n] == u and path[n+1] == v) or (path[n] == v and path[n+1] == u):
							num_on_path+=1			# if any of the adjacent nodes, adjaency found via n+1,
													# match our given [u,v] pair or conjugate [v,u], then we increment number of times this edge is on any path by 1 (num_on_path)
				between += num_on_path / len(paths[s][t])	# at the end of our path for-loop for a given [s,t] pair, increment betweenness by num_on_path divided by the length of the path
	return between											# ask why we do += num_on_path / len(paths[s][t]) and not just between = num_on_path

def edge_betweenness(nodes, edges, paths):
	# Create a dictionary based on given nodes, edges, and paths
	# this would be a nested function going through all edges and adding entries to each node unique pair
	B = {}
	for edge in edges:	# populate B dictionary with all edges, each default value of 0
		B[tuple(edge)] = 0 	# example: ('v1','v2') = 0 - jank way to convert to tuple

	for edge in edges:	# go through it again
		u, v = edge		# split edge into [u,v]
		B[tuple(edge)] = single_edge_betweenness(nodes, paths, u, v) # populate tuple entry with betweenness

	return B

def GN(nodes,edgelist,adjlist):
	partitions = [[nodes]]

	# WRITE CODE HERE
	
	return partitions

# keep this at the bottom of the file.
if __name__ == '__main__':
	main()
