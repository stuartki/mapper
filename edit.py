import os
import sys
from Node import Node
from reader import reader
import json

def writeToFile(file, data):
	open(file, "w").close()
	data= data[1:]
	data = [n.__dict__ for n in data]
	with open(file, "w") as current_file:
		current_file.write(json.dumps(data))

def edit(data):

	
	content = ""
	
	while content != "end":
		content = input("id: ")
		
		if content == "end":
			continue
		id = int(content)
		
		cur_node = data[id]
		cur = ""
		while cur != "end":
			cur = input(str(id) + ": ")
			if cur == "end":
				continue
			if cur == "ls":
				cur_node.printNode()
			if cur == "description":
				descrNew = input("\nid: " + str(id) + "\n" + str(cur_node.description) + "\n: ")
				if descrNew == "end":
					continue
				else:
					cur_node.description = descrNew
					print("\nid: " + str(id) + "\n" + str(cur_node.description))
			if cur == "past":
				p = ""
				while p != "end":

					p = input("\nid: " + str(id) + "\n" + ", "+ str(cur_node.past) + "\n\n: ")
					if p == "end":
						continue

					
					ind = p[0]
					newID = int(p[1:])
					
					if ind == "-":
						cur_node.past.remove(newID)
						data[newID].future.remove(id)
					if ind == "+":
						cur_node.past.append(newID)
						data[newID].future.append(id)
					print("\nid: " + str(id) + "\n" + ", " + str(cur_node.past))
			if cur == "future":

				p = ""
				while p != "end":

					p = input("\nid: " + str(id) + "\n" + ", "  + str(cur_node.future) + "\n\n: ")
					if p == "end":
						continue

				
					ind = p[0]
					newID = int(p[1:])
					print(newID)
					
					if ind == "-":
						cur_node.future.remove(newID)
						data[newID].past.remove(id)
					if ind == "+":
						cur_node.future.append(newID)
						data[newID].past.append(id)
					print("\nid: " + str(id) + "\n" + ", " + str(cur_node.future))
			if cur == "related":
				pa = ""
				while pa != "end":

					pa = input("\nid: " + str(id) + "\n" + ", ".join(cur_node.related) + "\n\n: ")
					if pa == "end":
						continue
					
					p = list(pa)
					if p[0] == "-":
						cur_node.related.remove(p[1])
						data[int(p[1])].related.remove(p[1])
					if p[0] == "+":
						cur_node.related.append(p[1])
						data[int(p[1])].related.append(p[1])
					print("\nid: " + str(id) + "\n" + ", ".join(cur_node.related))
			if cur == "keywords":

				pa = ""
				while pa != "end":

					pa = input("\nid: " + str(id) + "\n" + ", ".join(cur_node.keywords) + "\n\n: ")
					if pa == "end":
						continue
					
					p = list(pa)
					if p[0] == "-":
						cur_node.keywords.remove(p[1])
					if p[0] == "+":
						cur_node.keywords.append(p[1])	
					print("\nid: " + str(id) + "\n" + ", ".join(cur_node.keywords))
			if cur == "title":

				titleNew = input("\nid: " + str(id) + "\n" + cur_node.title + "\n\n: ")
				if titleNew == "end":
					continue
				else:
					cur_node.title = titleNew	
				print("\nid: " + str(id) + "\n" + cur_node.title)
# 			if cur == "type":
# 
# 				typeNew = input("\nid: " + str(id) + "\n" + cur_node.type + "\n\n: ")
# 				if descrNew == "end":
# 					continue
# 				else:
# 					cur_node.description = descrNew	
# 				print "\nid: " + str(id) + "\n" + cur_node.type
				
	return data
				