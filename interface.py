import os
import sys
from Node import Node
from reader import reader
from searcher import searcher, get, isCycle
from writer import writer
from edit import edit
from writer import writeToFile
from network import mostPopularSuc, mostPopularPred, init, draw_all, cleanPred, most_degree_centrality, labeler, getProject, printGraph
import json
import networkx as nx
import matplotlib.pyplot as plt

topic = ""

def reload(data):
	DG = init(data)
	#clean graph initially
	DG = cleanPred(data, DG)
	return DG
	

while topic != "end":
	#loading topic
	topic = input("topic: ")
	
	if topic == "end":
		continue
	if topic == "ls":
		for n in [n.replace(".json", "") for n in os.listdir("/Users/stuartki/Documents/connector/") if ".json" in n]:
			print(n)
		continue
	file = "/Users/stuartki/Documents/connector/" + topic + ".json"
	if topic + ".json" not in set(os.listdir("/Users/stuartki/Documents/connector/")):
		print("NEW")
		conf = input("confirm: ")
		#need a confirm option
		if conf == "y" or conf == "yes":
			with open(file, "w+") as cur_file:
				cur_file.write(json.dumps([]))
		else:
			continue
	
	start = ""
	data = reader(topic)
	DG = reload(data)
	#for the purpose of recording changes to length of dataset
	preLen = len(data)

	#actions
	while start != "end":
		start = input(topic + ": ")
		if start == "end":
			continue

		#print the new data? useless method because it writes to file everytime
		if start == "print":
			for i in range(preLen + 1, len(data)):
				print(str(data[i].id) + ": " + data[i].title)
				
			print(data)
			conf = input("confirm?: ")
			if conf == "y" or conf == "yes":
				writeToFile(file, data)
			else:
				continue

		if start == "edit":
			data = edit(data)
			writeToFile(file, data)
			DG = reload(data)

		#WRITING CONTENT
		if start == "write":
			writer(topic)
			data = reader(topic)
			DG = init(data)
			DG = cleanPred(data, DG)
		
		if start == "search":
			se = ""
			while se != "end":
				if se == "end":
					continue
				se = input("search: ")
				for n in searcher(se, data):
					print(str(n.id) + ": " + n.title)
					
		if start == "ls":
			for n in data:
				if isinstance(n, int):
					continue
				print(str(n.id) + ": " + str(n.title))
			
		if start == "graph":
			draw_all(data, DG)
			
		#summarize data
		#degree centrality, pred nodes, suc nodes (page rank)
		if start == "summarize":
			size = int(len(DG.nodes())/10)
			print("Size = " + str(size)) 
			centralnodes =  [n[0] for n in most_degree_centrality(DG, limit = size)]
			
			suc = mostPopularSuc(data, DG, limit = size)
			pred = mostPopularPred(data, DG, limit = size)
			
			totalNodes = []
			totalNodes.extend(centralnodes)
			totalNodes.extend(suc)
			totalNodes.extend(pred)
			
			print("Pred Nodes: ")
			print()
			for n in pred:
				print(str(n.id) + ": " + str(n.title))
			print()
			print("Central Nodes: ")
			print()
			for n in centralnodes:
				print(str(n.id) + ": " + str(n.title))
			print()
			print("Suc Nodes: ")
			print()
			for n in suc:
				print(str(n.id) + ": " + str(n.title))

			
			
			p = input("plot? ")
			if p == "y" or p == "yes":
				subDG = DG.subgraph(totalNodes)
				labels = labeler(data)
				pos = nx.spring_layout(subDG)
				labelDict = {n:lab for n,lab in labels.items() if n in pos}
				nx.draw(subDG, pos, with_labels = True, font_size = 12, labels = labelDict)
				plt.draw()
				plt.show()

		if start == "get":
			get(data)

		if start == "cycle":
			isCycle(DG)
			
		if start == "project":
			i = ""
			while i != "end":
				i = input("project: ")
				if i == "end":
					continue
				if i == "top":
					continue
				getProject(data, DG)
			
