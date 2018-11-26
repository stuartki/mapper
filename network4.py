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

def position(DG):
	marked = set()
	pos = {}
	def bfsPos(node, x, y):
		if node not in marked:

			marked.add(node)
			pos[node] = (x, y)
			count = 0
			for n in DG.successors(node):
				print count
				count = bfsPos(n, x + count, y + 10)
				print count
				print
				count += 10
			return count
	
	axioms = [n for n,d in DG.in_degree() if d == 0]
	
	
	c = 0
	for node in axioms:
		c = bfsPos(node, c, 0)
	
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

def printGraph(DG):
	marked = set()
	def bfsP(node, tab):
		marked.add(node)
		print tab + str(node.id) + ": " + node.title
		tab += "\t"
		for n in DG.successors(node):
			if n not in marked:
				
				bfsP(n, tab)
	
	axioms = [n for n,d in DG.in_degree() if d == 0]
	

	for node in axioms:
		bfsP(node, tab = "")
		
def getProject(data, DG):	
	leaves = [n for n,d in DG.out_degree() if d == 0]
	pred = [n for n,d in DG.in_degree() if d == 0]
	dict = {}
	marked = set()
	id = ""

	id = raw_input("InID: ")
	
	outID = raw_input("OutID: ")
	if id == "all" and outID == "all":

		for node in pred:
			s = set()
			for out in leaves:
				try:
					for a in nx.all_simple_paths(DG, node, out):
						for b in a:
							s.add(b)
				except:
					continue

			dict[node] = DG.subgraph(s)

	
	elif outID == "all" and id != "all":
		try:
			id = int(id)

			pp = data[id]
			s = set()
			for out in leaves:
				try:
					for a in nx.all_simple_paths(DG, pp, out):
						for b in a:
							s.add(b)
				except:
					continue

			dict[pp] = DG.subgraph(s)
		except:
			print "INVALID"
	elif id == "all" and outID != "all":
		try:
			outID = int(outID)

			out = data[outID]
			s = set()
			for p in pred:
				try:
					for a in nx.all_simple_paths(DG, p, out):
						for b in a:
							s.add(b)
				except:
					continue

			dict[p] = DG.subgraph(s)
		except:
			print "INVALID"
	else:
		outID = int(outID)
		inID = int(id)

		out = data[outID]
		i = data[inID]
		s = set()

		try:
			for a in nx.all_simple_paths(DG, i, out):
				for b in a:
					s.add(b)
		except:
			print "NO PATH"
		
		dict[i] = DG.subgraph(s)

			
	for n in dict.keys():
		printGraph(dict[n])
	return dict
		

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
indict = -2


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
