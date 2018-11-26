#writer
#what if we parse the description for keywords?

import os
import sys
from Node import Node
from readGrouper1 import reader
from editGrouper import edit
from searcher import searcher
import json
from network4 import mostPopularSuc, mostPopularPred, init,	draw_all, cleanPred, mostDegreeCentrality, labeler

def writeToFile(file, data):
	open(file, "w").close()
	data= data[1:]
	data = [n.__dict__ for n in data]
	with open(file, "w") as current_file:
		current_file.write(json.dumps(data))

def writer(topic, data = 0):
	def isint(s):
		try:
			int(s)
			return True
		except ValueError:
			return False
	
	def clean(data, curNode):

		for n in curNode.future:
			if n >= len(data):
				continue
			pastArray = data[n].past
			isThere = False
			for l in pastArray:
				if l == n:
					isThere = True
					break
			
			if not isThere:
				data[n].flashback(curNode.id)
		for n in curNode.past:
			if n >= len(data):
				continue
			futureArray = data[n].future
			isThere = False
			for l in futureArray:
				if l == n:
					isThere = True
					break
			
			if not isThere:
				data[n].flashforward(curNode.id)
		for n in curNode.related:
			if n >= len(data):
				continue
			relatedArray = data[n].related
			isThere = False
			for l in relatedArray:
				if l == n:
					isThere = True
					break
			
			if not isThere:
				data[n].relate(curNode.id)

	def summarize():
		centralnodes =  [n for n in mostDegreeCentrality(DG)[:10]]
		suc = mostPopularSuc(data, DG, limit = 10)
		pred = mostPopularPred(data, DG, limit = 10)
		
		centralnodes.extend(suc)
		centralnodes.extend(pred)
		
		
		p = raw_input("plot? ")
		if p == "y" or p == "yes":
			subDG = DG.subgraph(centralnodes)
			labels = labeler(data)
			pos = nx.spring_layout(subDG)
			labelDict = {n:lab for n,lab in labels.items() if n in pos}
			nx.draw(subDG, pos, with_labels = True, font_size = 12, labels = labelDict)
			plt.draw()
			plt.show()
	
	file = "/Users/stuartki/Documents/connector/" + topic + ".json"
	start = ""

	data = reader(topic)
	DG = init(data)
	DG = cleanPred(data, DG)
	
	
	if len(data) > 0:
		max = len(data)
	else: 
		max = 0


	content = ""
	summary = ""
	print topic + ".write"
	
	
	while content != "end":
		content = raw_input("")
		
		if content == "end":
			continue
		if content == "ls":
			print summary
			continue
		
		#enter
		if content == "":
			summary += "/"
			continue
		if content == "break":
			break
		#writing the actual content		
		summary += content + " "
	
	if content == "break":
		return ""
	#connecting the content
	
	print "Title: "
	title = raw_input("")
	
	print "Type: "
	type = []
	t = ""
	while t != "end":
		t = raw_input("")
		if t == "end":
			continue
		
		type.append(t)
	
	print "Past: "
	temp = ""
	back = []
	while temp != "end":
		temp  = raw_input("")
		if temp == "end":
			continue
		if temp == "ls":
			for n in data:
				if isinstance(n, int):
					continue
				print str(n.id) + ": " + str(n.title)
		if temp == "suc":
			for n in mostPopularSuc(data, DG, limit = 10):
				print str(n.id) + ": " + n.title
		if temp == "pre":
			for n in mostPopularPred(data, DG, limit = 10):
				print str(n.id) + ": " + n.title
		if temp == "cen":
			for n in mostDegreeCentrality(DG, limit = 10):
				print str(n[0].id) + ": " + n[0].title
		if isint(temp):
			result = int(temp)
			back.append(result)
		else:
			print [str(n.id) + ": " + str(n.title) for n in searcher(temp, data)]
		print back
	print "Future: "
	temp = ""
	future = []
	while temp != "end":
		temp  = raw_input("")
		if temp == "end":
			continue
		if temp == "ls":
			for n in data:
				if isinstance(n, int):
					continue
				print str(n.id) + ": " + str(n.title)
		if temp == "suc":
			for n in mostPopularSuc(data, DG, limit = 10):
				print str(n.id) + ": " + n.title
		if temp == "pre":
			for n in mostPopularPred(data, DG, limit = 10):
				print str(n.id) + ": " + n.title
		if temp == "cen":
			for n in mostDegreeCentrality(DG, limit = 10):
				print str(n[0].id) + ": " + n[0].title
		if isint(temp):
			result = int(temp)
			future.append(result)
		else:
			print [str(n.id) + ": " + str(n.title) for n in searcher(temp, data)]
		print future
	
	c = ""
	related = []
	keyword = []
	while c != "end":
		c = raw_input("")
		if c == "end":
			continue
		if c == "break":
			break
		if c == "related":
			print "Related: "
			temp = ""
			while temp != "end":
				temp  = raw_input("")
				if temp == "end":
					continue
				if isint(temp):
					result = int(temp)
					related.append(result)
				else:
					print [str(n.id) + ": " + str(n.title) for n in searcher(temp, data)]
				print related
		if c == "keywords":
			print "Keywords: "
			temp = ""
			while temp != "end":
				temp  = raw_input("")
				if temp == "end":
					continue
				keyword.append(temp)
		if c == "edit":
			data = edit(data)
	if c == "break":
		return ""
	print title
	print type
	print summary
		
	#CLEANING
	
	current_Node = Node(title, type, summary, keyword, back, future, related, max)
	
	clean(data, current_Node)
			
	
	data.append(current_Node)
	max += 1
	#WRITING BACK TO TXT FILE
	writeToFile(file, data)
			

			
			
		

