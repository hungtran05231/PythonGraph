import networkx as nx
from networkx.algorithms import bipartite

def is_triangle(G):
	if(nx.number_of_nodes(G)==3):
		for node in nx.nodes(G):
			if(nx.degree(G,node)!=2):
				return False
		return True
	return False

def is_star(G):
	if(nx.is_bipartite(G)):
		X,Y = bipartite.sets(G)
		if(len(list(X))==1 or len(list(Y))==1):
			return True
	return False

def is_leaf(G, node):
	return nx.degree(G,node)==1

def is_leaf_adjacent(G, node):
	for item in G.neighbors(node):
		if(is_leaf(G, item)):
			return True
	return False

def add_mim_and_delete_adjacent_leaf(G, node, mim):
	added=0
	for item in G.neighbors(node):
		if(is_leaf(G, item)):
			edge=[]
			edge.append(node)
			edge.append(item)
			if(added==0):
				mim.append(edge)
				added=1
			G.remove_node(item)

def is_triangle_edge(G, edge):
	if(nx.degree(G,edge[0])==2 and nx.degree(G,edge[1])==2):
		return True
	return False

def triangle_attack_node(G, edge):
	for item in nx.common_neighbors(G, edge[0], edge[1]):
		return item

def delete_triangle(G, edge):
	G.remove_node(edge[0])
	G.remove_node(edge[1])

def is_equal(G, color1, color2):
	for node in G.nodes():
		if(color1[node]!=color2[node]):
			return False
	return True

def is_complete_different(G, color1, color2):
	for node in G.nodes():
		if(color1[node]==color2[node]):
			return False
	return True

def is_im_equal_m(G, color1):
	if(nx.is_bipartite(G)):
		color2 = bipartite.color(G)
		print(color2)
		return (is_equal(G,color1,color2) or is_complete_different(G, color1, color2))
	return False

def construct_mim_and_reduce_nodes(G):
	mim = []
	color1 = {}
	for node in G.nodes():
		color1[node]=1
	triangle_edges = []	
	for edge in G.edges():
		if(is_triangle_edge(G, edge)):
			if(is_leaf_adjacent(G, triangle_attack_node(G,edge))):
				print("im and m is differ")
				return
			triangle_edges.append(edge)
	for node in G.nodes():
		if(is_leaf_adjacent(G, node)):
			color1[node]=0
	for node in G.nodes():
		if(color1[node]==0):
			add_mim_and_delete_adjacent_leaf(G, node, mim)
	for edge in triangle_edges:
		delete_triangle(G,edge)
	mim.extend(triangle_edges)
	if(is_im_equal_m(G, color1)):
		return mim
	else:
		print("im and m is differ")
		return

G = nx.Graph()
G.add_edge(1,2)
G.add_edge(0,3)
G.add_edge(2,4)
G.add_edge(3,5)
G.add_edge(2,6)
G.add_edge(2,7)
G.add_edge(0,9)
G.add_edge(0,10)
G.add_edge(9,10)
G.add_edge(11,12)
G.add_edge(11,1)
G.add_edge(12,1)
G.add_edge(13,3)
G.add_edge(14,3)
print(construct_mim_and_reduce_nodes(G))

