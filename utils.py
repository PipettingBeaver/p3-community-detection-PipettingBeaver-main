import sys
import copy
import random
from pyvis.network import Network

#######
## Given an adjacency list, computes the shortest paths for
## all pairs of nodes in the graph.
## Inputs: adj_list (dictionary) - adjacency list
## Returns: paths (dictionary) - object where the list of paths
## for two nodes u and v can be accessed using paths[u][v] or paths[v][u]
#######
def all_pairs_shortest_paths(adj_list):
	paths = {}
	for u in adj_list: # for every node...
		paths[u] = {}
		# get shortest paths & node predecessors from this node
		dist,predecessors = shortest_paths(adj_list,u)

		# get the paths for nodes with a non-inf or non-zero distance.
		for v in dist:
			if u == v or dist[v]==float('inf'):
				paths[u][v] = []
			else:
				paths[u][v] = get_paths(predecessors,v,[[v]])
	return paths

#######
## Computes the shortest paths from n to all other
## nodes. Modified from Lab 3 to return a predecessor dictionary as well.
## Inputs: adj_list (dictionary) - adjacency list
## Inputs: n (string) - node
## Returns: distance dictionary (u:distance) for every node u
## Returns: predecessors dictionary (u:[pred list]) for every node u
#######
def shortest_paths(adj_list, n):
	# initialize distances dictionary & predecessors dictionary
	dist = {n:float('inf') for n in adj_list.keys()}
	predecessors = {n:[] for n in adj_list.keys()}
	dist[n] = 0
	predecessors[n] = None

	# initialize to_explore list
	to_explore = [n]

	while len(to_explore) > 0: # while there's still a node to explore...
		exploring = to_explore.pop(0) # remove the FIRST node from to_explore

		# for every neighbor, check if it has been visited
		for neighbor in adj_list[exploring]:
			if dist[neighbor] == float('inf'): # unexplored
				# update the distance to neighbor
				dist[neighbor] = dist[exploring] + 1
				# update where we came from.
				predecessors[neighbor].append(exploring)
				# add neighbor to the to_explore list
				to_explore.append(neighbor)
			# catch ties and add predecessors
			elif dist[neighbor] == dist[exploring]+1:
				predecessors[neighbor].append(exploring)
	return dist,predecessors

#######
## Recursive function that calculates all possible shortest paths
## for a node based on the predecessors from shortest_paths() function.
## It is called for the LAST node in the path and traces paths backwards.
## Inputs: predecessors dictionary
## Inputs: current node n to process
## Inputs: current paths list (paths from the end traced back to n)
## Returns: List of paths, where each path is a list of nodes
#######
def get_paths(predecessors,n,curr_paths):
	# base case
	# we've reached the first node; we're done.
	if predecessors[n] == None:
		return curr_paths

	# there's still at least one node to backtrack.
	# for each predecessor, prepend the predecessor and call
	# get_paths() for the predecessor.
	new_paths = []
	for pred in predecessors[n]:
		these_paths = []
		for i in range(len(curr_paths)):
			these_paths.append([pred]+curr_paths[i])
		new_paths+=get_paths(predecessors,pred,these_paths)
	return new_paths


#######
## Removes an edge from an edgelist.
#######
def remove_from_edgelist(edge,edge_list):
	# get edge from edge list. Could be (u,v) or (v,u)
	u = edge[0]
	v = edge[1]
	options = [(u,v),(v,u),[u,v],[v,u]]
	for e in options:
		if e in edge_list:
			edge_list.remove(e)
	## returns nothing - removes in-place
	return

#######
## Removes an edge from an adjacency list.
#######
def remove_from_adjlist(edge,adj_list):
	u = edge[0]
	v = edge[1]
	adj_list[u].remove(v)
	adj_list[v].remove(u)
	## returns nothing - removes in-place
	return

#######
## Given a partition, a current group, and the group divided in two,
## returns a new partition with the current group removed and
## the two split groups added.
#######
def split_partition(prev_partition,split1,split2):
	partition = copy.deepcopy(prev_partition) # make a copy of partition
	list_to_remove = []
	before = split1+split2
	for p in partition:
		if sorted(p)==sorted(before):
			list_to_remove = p
	partition.remove(list_to_remove)
	partition.append(sorted(split1))
	partition.append(sorted(split2))
	return partition

#######
## Given an adjacency list and a node u, 
## returns a sorted list of nodes that are 
## in the same connected component as u.
#######
def conncomp(adjlist,u):
	# initialize a queue Q and a set of seen nodes
	Q = [u]
	seen = set()
	seen.add(u)

	while len(Q) > 0: # while there's still a node to explore...
		exploring = Q.pop(0) # remove the FIRST node from Q
		for neighbor in adjlist[exploring]:
			if neighbor not in seen: # unexplored
				seen.add(neighbor) # add the neighbor to the seen node set
				Q.append(neighbor) # append the neighbor to Q
	return sorted(list(seen))

## RGB to Hex function - copied from Lab 2
def rgb_to_hex(red,green,blue): # pass in three values between 0 and 1
  maxHexValue= 255  ## max two-digit hex value (0-indexed)
  r = int(red*maxHexValue)    ## rescale red
  g = int(green*maxHexValue)  ## rescale green
  b = int(blue*maxHexValue)   ## rescale blue
  RR = format(r,'02x') ## two-digit hex representation
  GG = format(g,'02x') ## two-digit hex representation
  BB = format(b,'02x') ## two-digit hex representation
  return '#'+RR+GG+BB

## visualize the graph.
def viz_example(nodes,edges,partition,outfile):
	"""
	Visualize a graph and write it to an HTML file.
	:param: nodes - list or set of nodes
	:param: edges - list of 2-element lists.
	:param: partition - list of lists representing a partition of the nodes to color.
	:param: outfile - string outfile that ends in '.html'
	:returns: None
	"""
	# Refer to Lab 1 for instructions about visualizing a graph.

	# get colors for partitions
	node_colors = {}
	for cluster in partition:
		color = rgb_to_hex(random.random(),random.random(),random.random())
		for n in cluster:
			node_colors[n] = color

	G = Network() # create graph
	for n in nodes: # add nodes
		G.add_node(n,label=n,color=node_colors[n])
	for u,v in edges: # add edges
		G.add_edge(u,v) 

	G.toggle_physics(True) 
	G.show_buttons(filter_=['physics'])

	G.write_html(outfile)
	print('Saved file as',outfile)

	return
