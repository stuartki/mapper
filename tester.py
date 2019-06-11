import networkx as nx
import matplotlib.pyplot as plt
from Node import Node
import json
from writer import writeToFile
from reader import reader
from network import init

# def position(DG):
# 	marked = set()
# 	pos = {}
# 	def bfsPos(node, x, y):
# 		if node not in marked:

# 			marked.add(node)
# 			pos[node] = (x, y)
# 			count = 0
# 			for n in DG.successors(node):
# 				print count
# 				count = bfsPos(n, x + count, y + 10)
# 				print count
# 				print
# 				count += 10
# 			return count
	
# 	axioms = [n for n,d in DG.in_degree() if d == 0]
	
	
# 	c = 0
# 	for node in axioms:
# 		c = bfsPos(node, c, 0)
		
		
# 	return pos
# # 
# G = nx.Graph()
# 
# G.add_nodes_from([0, 1, 2, 3])
# 
# nx.draw(G, pos, with_labels = True)
# 
# plt.show()

def clean_numbers(topic):
	file = "/Users/stuartki/Documents/connector/" + topic + ".json"
	tempData = []

	with open(file, "r") as current_file:
		tempData = json.load(current_file)

	max = len(tempData)
	if max == 0:
		max += 1

	data = [max]


	#turning the lines into nodes
	id = 0
	past = []
	title = ""
	type = ""
	future = []
	description = ""
	keywords = []
	related = []

	for line in tempData:
		count = 0
	
	
		#ID = 0, PAST = 1, FUTURE = 2, KEYWORDS = 3, DESCRIPTION = 4, 
	
		id = int(line["id"])
		past = [int(n) for n in line["past"] if n != '']
		title = line["title"]
		type = line["type"]
		future = [int(n) for n in line["future"] if n != '']
		description = line["description"]
		keywords = line["keywords"]
		related = [int(n) for n in line["related"] if n != '']
		
	
		current_node = Node(title, type, description, keywords, past, future, related, id)
		data.append(current_node)
	writeToFile(file, data)
	return data

def method_edge_counter(topic):
	d = reader(topic)
	count = 0
	for n in d:
		if isinstance(n, int):
			continue
		count+= len(n.past)
	return count

data = reader('probability')
DG = init(data)
G = nx.Graph(DG)
import community
partition = community.best_partition(G)
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))



nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()



