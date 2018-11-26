import networkx as nx
import os
import sys
from Node import Node
from readGrouper1 import reader
from editGrouper import edit
import matplotlib.pyplot as plt
import operator
from collections import Counter
import pandas as pd
from tester import position



## create new position indicator



def labeler(data):
	labels = {}
	for node in data:
		if type(node) is int:
			continue
		la = node.title + "\n" + str(node.id)
		labels[node] = la
	return labels	

def bfs(node, data, DG):
	startArray = [node]
	marked = set()
	for x in startArray:
		if x in marked:
			continue
		marked.add(x)
		
		for n in x.past:
			if n == '':
				continue
			cur = data[int(n)]
			if cur in marked:
				continue
			
			startArray.append(cur)
		for n in x.future:
			if n == '':
				continue
			cur = data[int(n)]
			if cur in marked:
				continue
			
			startArray.append(cur)
	return startArray
def dictSorter(dict, rev = ""):
	if rev == "reverse":
		r = True
	else:
		r = False
	sorted_x = sorted(dict.items(), key=operator.itemgetter(1), reverse = r)
	return sorted_x		


	
# initialize DG	
def init(d):
	def mark(node, data, DG):
		for x in node.past:
			if x == '':
				continue
			DG.add_node(data[int(x)], title = data[int(x)].title)
			DG.add_edge(data[int(x)], node)
		for x in node.future:
			if x == '':
				continue
			DG.add_node(data[int(x)], title = data[int(x)].title)
			DG.add_edge(node, data[int(x)])	
	DG = nx.DiGraph()	
	for node in d:
		if type(node) != Node:
			continue
		DG.add_node(node, title = node.title, id = node.id)
		mark(node, d, DG)
	return DG	

def mostDegreeCentrality(DG, limit = 0):
	list = [(k, round(v, 2)) for k, v in nx.degree_centrality(DG).items()]
	lol = sorted(list, key = lambda x : x[1], reverse = True)
	
	
	if limit != 0:
		lol = lol[:limit]
	return lol

def tier(DG):
	shortPath = nx.shortest_path(DG)
	tierDict = {}
	for k, v in shortPath.items():
		sourceDict = {}
		for key, value in v.items():
			
			if len(value) in sourceDict.keys():
				va = sourceDict[len(value)]
				va.append(key)
				sourceDict[len(value)] = va
			else:
				sourceDict[len(value)] = [key]

		tierDict[k] = sourceDict
	return tierDict

def cleanPred(data, graph):
	count = 0
	counter = 0
	for node in data:
		if count == 0:
			count += 1
			continue
		setM = set()
		for n in graph.predecessors(node):
			if len(list(nx.all_simple_paths(graph, n, node))) > 1:
				counter += 1
#				print "ids: " + node.id +", " + n.id
				setM.add(n)
		for x in setM:
			graph.remove_edge(x, node)
		

#	print "DELETED " + str(counter) + " EDGES"
	return graph

def allpredecessors(DG, node):
	returnArray = []
	marked = set()
	def recurPred(cur_node):
		for n in DG.predecessors(cur_node):
			if n in marked:
				continue
			marked.add(n)
			returnArray.append(n)
			recurPred(n)
	recurPred(node)
	return returnArray
	
def allsuccessors(DG, node):
	returnArray = []
	marked = set()
	def recurSuc(cur_node):
		for n in DG.successors(cur_node):
			if n in marked:
				continue
			marked.add(n)
			returnArray.append(n)
			recurSuc(n)
	recurSuc(node)
	return returnArray

#could also weight them by tier
def mostPopularPred(data, DG, limit = 0, plot = False):
	histArray = []
	count = 0
	for n in DG.nodes():
		count += 1
		if isinstance(n, int):
			continue
		histArray.extend([n.id for n in allpredecessors(DG, n)])
	h = pd.Series(histArray)
	hi = h.value_counts()
	if limit != 0:
		hi = hi[:limit]
	tempD = hi.reset_index()
	tempSeries = tempD.iloc[:, 0:1]
	returnArray = [data[int(n)] for n in tempSeries.values]
	if plot:
		hi.plot(kind = "bar")
		plt.tight_layout()
		plt.show()
	return returnArray
	
def mostPopularSuc(data, DG, limit = 0, plot = False):
	histArray = []
	count = 0
	for n in DG.nodes():
		if isinstance(n, int):
			continue
		histArray.extend([n.id for n in allsuccessors(DG, n)])
	h = pd.Series(histArray)
	hi = h.value_counts()
	if limit != 0:
		hi = hi[:limit]
	
	tempD = hi.reset_index()
	tempSeries = tempD.iloc[:, 0:1]
	returnArray = [data[int(n)] for n in tempSeries.values]

	if plot:
		hi.plot(kind = "bar")
		plt.tight_layout()
		plt.show()
	return returnArray

def lenPred(data):
	rankDict = {}
	for n in data:
		if isinstance(n, int):
			continue
		rankDict[n] = len(allpredecessors(DG, n))
	ranks = dictSorter(rankDict, rev = "reverse")
	return ranks

def lenSuc(data):
	rankDict = {}
	for n in data:
		if isinstance(n, int):
			continue
		rankDict[n] = len(allsuccessors(DG, n))
	ranks = dictSorter(rankDict, rev = "reverse")
	return ranks

def draw_all(data, DG):
	#nx.draw(DG, with_labels = False, node_size = 150, font_size = 4)
	pos = nx.spring_layout(DG)
	labels = labeler(data)
	labelDict = {n:lab for n,lab in labels.items() if n in pos}
	nx.draw(DG, pos, with_labels = True, alpha = 0.8, node_size = 500, node_color = "black", edge_color = "blue",
		font_color = "red", font_size = 10, font_weight = "bold", labels = labelDict)

# 	plt.style.use('ggplot')
	plt.draw()
	plt.show()
			
def draw_current(data, id, DG):
	
	cur_node = data[int(id)]
	labels = labeler(data)
	
	
	subgraphA = [cur_node]
	pred = 	list(DG.predecessors(cur_node))
	succ = list(DG.successors(cur_node))
	subgraphA.extend(pred)
	subgraphA.extend(succ)

	subDG = DG.subgraph(subgraphA)
	pos = nx.spring_layout(subDG)
	labelDict = {n:lab for n,lab in labels.items() if n in pos}
	nx.draw(subDG, pos, with_labels = True, font_size = 12, labels = labelDict)
	plt.draw()
	plt.show()
		
def draw_subgraph(data, subg, DG):
	id = ""
	labels = labeler(data)
	while id != "end":
		id = raw_input("id: ")
		if id == "break":
			break
		if id == "end":
			continue
		if id == "edit":
			edit(topic)
			
		subgraphA = []
		
		cur_node = data[int(id)]
		subgraphA.extend(bfs(cur_node, DG))
		subDG = DG.subgraph(subgraphA)		
#  		print str(len(subgraphA)) + " NODES"
		pos = nx.spring_layout(subDG)
		labelDict = {n:lab for n,lab in labels.items() if n in pos}
		nx.draw(subDG, pos, with_labels = True, font_size = 12, labels = labelDict)
		plt.draw()
		plt.show()
		
def deleteIsolates(DG):
	subgraph = []
	count = 0
	for n in DG.nodes():
		if len(DG.in_edges(n)) == 0 and len(DG.out_edges(n)) == 0:
			count += 1
			continue
		else:
			subgraph.append(n)
	print str(count) + " NODES DELETED"
	return DG.subgraph(subgraph)	

# topic = raw_input("topic: ")
# 
# data = reader(topic)
# DG = init(data)



##WORKSPACE
indict = 2


if indict == -1:
	topic = "informationTheory"

	data = reader(topic)
	DG = init(data)
	print [(n.title, v) for n, v in position(DG).items()]
	nx.draw(DG, position(DG))
	plt.show()

if indict == 1:
#	[n for n in nx.strongly_connected_components(DG) if len(n) > 1 ]
# 	n = [(lenSuc()[n][0].id, round(nx.degree_centrality(DG)[data[int(lenSuc()[n][0].id)]] * 100., 2)) for n in range(0,10)]
# 	s = sorted(n, key=operator.itemgetter(1))
#	print axiomer(data)
	

	cleanPred(DG)
	print nx.info(DG)
	print [n.id for n in mostPopularPred(DG, limit = 10)]
	for n in mostPopularPred(DG, limit = 10):
		DG.remove_node(n)
	print nx.info(DG)
	print [n.id for n in mostPopularPred(DG, limit = 10)]
	for n in mostPopularPred(DG, limit = 10):
		DG.remove_node(n)
	print nx.info(DG)
	print [n.id for n in mostPopularPred(DG, limit = 10)]
	
	sys.exit()
	
if indict == 2:
	topic = "informationTheory"

	data = reader(topic)
	DG = init(data)
	print [n.title for n,d in DG.in_degree() if d == 0]
	print [n.title for n,d in DG.out_degree() if d == 0]
		
		
		
		
		
	sys.exit()

if indict == 3:
	centralnodes =  [n for n in mostDegreeCentrality(DG)[:10]]
	centralnodes.extend(mostPopularSuc(DG, limit = 10))
	centralnodes.extend(mostPopularPred(DG, limit = 10))
	
	subDG = DG.subgraph(centralnodes)
	pos = nx.spring_layout(subDG)
	labelDict = {n:lab for n,lab in labels.items() if n in pos}
	nx.draw(subDG, pos, with_labels = True, font_size = 12, labels = labelDict)
	plt.draw()
	plt.show()

	sys.exit()
	
if indict == 4:
	print [n.title for n in mostPopularSuc(DG, limit = 10)]
	sys.exit()
##WORKSPACE

if indict == 5:
	topic = "informationTheory"

	data = reader(topic)
	DG = init(data)
	DG = deleteIsolates(DG)
	print nx.info(DG)
	
	dict = {}
	for node in [n for n,d in DG.in_degree() if d == 0]:
		s = set()
		for out in [n for n,d in DG.out_degree() if d == 0]:
			try:
				for a in nx.all_simple_paths(DG, node, out):
					for b in a:
						s.add(b)
			except:
				continue

		dict[node] = s
	
	returnDict = {}
	for node in [n for n,d in DG.in_degree() if d == 0]:
		for com_node in [n for n,d in DG.in_degree() if d == 0]:
			if node == com_node:
				continue
			for x in dict[node]:
				if x in dict[com_node]:
					if x in returnDict.keys():
						returnDict[x] += 1
					else:
						returnDict[x] = 1
	print len(dict)
	print [n[0].title for n in dictSorter(returnDict, rev = "reverse")[:5]]


if indict == 0:
	topic = raw_input("topic: ")

	data = reader(topic)
	DG = init(data)

	cur = ""
	cleanPred(data, DG)
	while cur != "end":
		if id == "edit":
			edit(topic)
		cur = raw_input("graph: ")
		if cur == "cur":
			id = ""
			while id != "end":
				id = raw_input("id: ")
				if id == "end":
					continue
				if id == "edit":
					edit(topic)

				draw_current(data, id, DG)
		if cur == "sub":
			draw_subgraph(data, [], DG)
		if cur == "all":
			draw_all(data, DG)
		if cur == "end":
			continue