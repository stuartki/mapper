#writer
#what if we parse the description for keywords?

import os
import sys
from Node import Node
from readGrouper import reader
from editGrouper import edit
from searcher import searcher

import json

def writer(topic):
	def isint(s):
		try:
			int(s)
			return True
		except ValueError:
			return False
	file = "/Users/stuartki/Documents/connector/" + topic + ".json"
	start = ""
	data = reader(topic)
	if len(data) > 0:
		max = len(data)

	else: 
		max = 0

	
	while start != "end":
		start = raw_input(topic + ": ")
		
		if start == "edit":
			data = edit(data)

		#WRITING CONTENT
		if start == "write":
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
					continue
				#writing the actual content		
				summary += content + " "
			
			if content == "break":
				break
			#connecting the content
			
			print "Title: "
			title = raw_input("")
			
			print "Type: "
			type = raw_input("")
			
			print "Past: "
			temp = ""
			back = []
			while temp != "end":
				temp  = raw_input("")
				if temp == "end":
					continue
				if isint(temp):
					result = int(temp)
					past.append(result)
				
				print [str(n.id) + ": " + str(n.title) for n in searcher(temp, data)]
				print past
			print "Future: "
			temp = ""
			future = []
			while temp != "end":
				temp  = raw_input("")
				if temp == "end":
					continue
				if isint(temp):
					result = int(temp)
					future.append(result)
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
					continue
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
				break
			print title
			print type
			print summary
				
			#CLEANING
			
			for n in future:
				if n >= len(data):
					continue
				pastArray = data[n].past
				isThere = False
				for l in pastArray:
					if l == n:
						isThere = True
				
				if not isThere:
					data[n].flashback(max)
			for n in back:
				if n >= len(data):
					continue
				futureArray = data[n].future
				isThere = False
				for l in futureArray:
					if l == n:
						isThere = True
				
				if not isThere:
					data[n].flashforward(max)
			for n in related:
				if n >= len(data):
					continue
				relatedArray = data[n].related
				isThere = False
				for l in relatedArray:
					if l == n:
						isThere = True
				
				if not isThere:
					data[n].relate(max)
					
					
			
			
			
			current_Node = Node(title, type, summary, keyword, back, future, related, max)
			data.append(current_Node)
			max += 1
	#WRITING BACK TO TXT FILE
	
	open(file, 'w').close()
	data= data[1:]
	data = [n.__dict__ for n in data]
	with open(file, "w") as current_file:
		current_file.write(json.dumps(data))
			

			
			
		

