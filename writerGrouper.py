#writer
#what if we parse the description for keywords?

import os
import sys
from Node import Node
from readGrouper import reader

def writer(topic):
	file = "/Users/stuartki/Documents/connector/" + topic + ".txt"
	start = ""
	data = reader(topic)
	if len(data) > 0:
		max = data[0]

	else: 
		max = 0

	
	while start != "end":
		start = raw_input(topic + ": ")
		
		#WRITING CONTENT
		if start == "write":
			content = ""
			summary = ""
			print topic + ".write"
			
			
			while content != "end":
				content = raw_input("")
				
				if content == "end":
					summary + "\n"
					continue
				if content == "ls":
					print summary
					continue
				
				#enter
				if content == "":
					summary += "/"
					continue
					
				if content == "^X":
					break
						
				#writing the actual content		
				summary += content + " "
			
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
				result = int(temp)
				back.append(result)
			
			print "Future: "
			temp = ""
			future = []
			while temp != "end":
				temp  = raw_input("")
				if temp == "end":
					continue
				result = int(temp)
				future.append(result)
			
			print "Related: "
			temp = ""
			related = []
			while temp != "end":
				temp  = raw_input("")
				if temp == "end":
					continue
				result = int(temp)
				related.append(result)
			
			print "Keywords: "
			temp = ""
			keyword = []
			while temp != "end":
				temp  = raw_input("")
				if temp == "end":
					continue
				keyword.append(temp)
			
			print title
			print type
			print back
			print future
			print summary
			print keyword
				
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
	
	for n in data:
		if isinstance(n, (int, long)):
			with open(file, "a+") as current_file:
				current_file.write(str(max) + "\n")
			continue
		
	
		with open(file, "a+") as current_file:
		
			#write ID

			current_file.write(str(n.id))
			current_file.write(",")
			
			
			#write TITLE
			current_file.write(str(n.title))
			current_file.write(",")
			
			
			#WRITE TYPE
			current_file.write(str(n.type))
			current_file.write(",")
			
			
			#write PAST
			count = 0
			for item in n.past:
				count+=1
				if count == len(n.past):
					current_file.write(str(item))
					continue
				current_file.write(str(item) + "|")
			current_file.write(",")
			#write FUTURE
			count = 0
			for item in n.future:
				count +=1
				if count == len(n.future):
					current_file.write(str(item))
					continue
				current_file.write(str(item) + "|")
			current_file.write(",")
			#write RELATED
			count = 0
			for item in n.related:
				count +=1
				if count == len(n.related):
					current_file.write(str(item))
					continue
				current_file.write(str(item) + "|")
			current_file.write(",")
			#write KEYWORD
			count = 0
			for item in n.keywords:
				count +=1
				if count == len(n.keywords):
					current_file.write(str(item))
					continue
				current_file.write(str(item) + "|")
			current_file.write(",")
			#write DESCRIPTION
			current_file.write(n.description)
	
	with open(file, "a+") as current_file:
		current_file.write("\n")
			

			
			
		

