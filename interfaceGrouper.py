import os
import sys
from Node import Node
from readGrouper1 import reader
from editGrouper import edit
from searcher import searcher, get
from writerGrouper4 import writer
from writerGrouper4 import writeToFile
from network4 import mostPopularSuc, mostPopularPred, init, draw_all, cleanPred, mostDegreeCentrality, labeler, getProject, printGraph
import json
import networkx as nx
import matplotlib.pyplot as plt

topic = ""

while topic != "end":
	topic = raw_input("topic: ")
	
	if topic == "end":
		continue

	file = "/Users/stuartki/Documents/connector/" + topic + ".json"

	if topic + ".json" not in set(os.listdir("/Users/stuartki/Documents/connector/")):
		print "NEW"
		conf = raw_input("confirm: ")
		if conf == "y" or conf == "yes":
			with open(file, "w+") as cur_file:
				cur_file.write(json.dumps([]))
		else:
			continue

	start = ""
	data = reader(topic)
	DG = init(data)
	DG = cleanPred(data, DG)

	preLen = len(data)

	while start != "end":
		start = raw_input(topic + ": ")
		if start == "end":
			continue

		if start == "print":
			for i in range(preLen + 1, len(data)):
				print str(data[i].id) + ": " + data[i].title
				
			print data
			conf = raw_input("confirm?: ")
			if conf == "y" or conf == "yes":
				writeToFile(file, data)
			else:
				continue

		if start == "edit":
			data = edit(data)
			writeToFile(file, data)
			DG = init(data)
			DG = cleanPred(data, DG)

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
				se = raw_input("search: ")
				for n in searcher(se, data):
					print str(n.id) + ": " + n.title
					
		if start == "ls":
			for n in data:
				if isinstance(n, int):
					continue
				print str(n.id) + ": " + str(n.title)
			
		if start == "graph":
			draw_all(data, DG)
			
		if start == "summarize":
			size = int(len(DG.nodes())/10)
			print "Size = " + str(size)
			centralnodes =  [n[0] for n in mostDegreeCentrality(DG, limit = size)]
			
			suc = mostPopularSuc(data, DG, limit = size)
			pred = mostPopularPred(data, DG, limit = size)
			
			totalNodes = []
			totalNodes.extend(centralnodes)
			totalNodes.extend(suc)
			totalNodes.extend(pred)
			
			print "Pred Nodes: "
			print
			for n in pred:
				print str(n.id) + ": " + str(n.title)
			print
			print "Central Nodes: "
			print 
			for n in centralnodes:
				print str(n.id) + ": " + str(n.title)
			print
			print "Suc Nodes: "
			print
			for n in suc:
				print str(n.id) + ": " + str(n.title)

			
			
			p = raw_input("plot? ")
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
			
		if start == "project":
			input = ""
			while input != "end":
				input = raw_input("Project: ")
				if input == "end":
					continue
				getProject(data, DG)
			




	
