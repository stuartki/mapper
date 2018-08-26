import os
import sys
from Node import Node
from readGrouper import reader

def edit(topic):
	file = "/Users/stuartki/Documents/connector/" + topic + ".txt"
	start = ""
	data = reader(topic)
	
	content = ""
	
	while content != "end":
		content = raw_input("id: ")
		
		if content == "end":
			continue
		id = int(content)
		
		cur_node = data[id]
		cur = ""
		while cur != "end":
			cur = raw_input(str(id) + ": ")
			if cur == "description":
				descrNew = raw_input("\nid: " + str(id) + "\n" + str(cur_node.description) + "\n: ")
				if descrNew == "end":
					continue
				else:
					cur_node.description = descrNew
					print "\nid: " + str(id) + "\n" + str(cur_node.description)
			if cur == "past":
				pa = ""
				while pa != "end":
					if pa == "end":
						continue
					pa = raw_input("\nid: " + str(id) + "\n" + ", ".join(cur_node.past) + "\n\n: ")
					p = list(pa)
					if p[0] == "-":
						cur_node.past.remove(p[1])
						data[int(p[1])].future.remove(p[1])
					if p[0] == "+":
						cur_node.past.append(p[1])
						data[int(p[1])].future.append(p[1])
					print "\nid: " + str(id) + "\n" + ", ".join(cur_node.past)
			if cur == "future":

				pa = ""
				while pa != "end":
					if pa == "end":
						continue
					pa = raw_input("\nid: " + str(id) + "\n" + ", ".join(cur_node.future) + "\n\n: ")
					p = list(pa)
					if p[0] == "-":
						cur_node.future.remove(p[1])
						data[int(p[1])].past.remove(p[1])
					if p[0] == "+":
						cur_node.future.append(p[1])
						data[int(p[1])].past.append(p[1])
					print "\nid: " + str(id) + "\n" + ", ".join(cur_node.future)
			if cur == "related":

				pa = ""
				while pa != "end":
					if pa == "end":
						continue
					pa = raw_input("\nid: " + str(id) + "\n" + ", ".join(cur_node.related) + "\n\n: ")
					p = list(pa)
					if p[0] == "-":
						cur_node.related.remove(p[1])
						data[int(p[1])].related.remove(p[1])
					if p[0] == "+":
						cur_node.related.append(p[1])
						data[int(p[1])].related.append(p[1])
					print "\nid: " + str(id) + "\n" + ", ".join(cur_node.related)
			if cur == "keywords":

				pa = ""
				while pa != "end":
					if pa == "end":
						continue
					pa = raw_input("\nid: " + str(id) + "\n" + ", ".join(cur_node.keywords) + "\n\n: ")
					p = list(pa)
					if p[0] == "-":
						cur_node.keywords.remove(p[1])
					if p[0] == "+":
						cur_node.keywords.append(p[1])	
					print "\nid: " + str(id) + "\n" + ", ".join(cur_node.keywords)
			if cur == "title":

				descrNew = raw_input("\nid: " + str(id) + "\n" + cur_node.title + "\n\n: ")
				if descrNew == "end":
					continue
				else:
					cur_node.description = descrNew	
				print "\nid: " + str(id) + "\n" + cur_node.title
			if cur == "type":

				descrNew = raw_input("\nid: " + str(id) + "\n" + cur_node.type + "\n\n: ")
				if descrNew == "end":
					continue
				else:
					cur_node.description = descrNew	
				print "\nid: " + str(id) + "\n" + cur_node.type
				
		
	open(file, 'w').close()			
	max = data[0]
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
				