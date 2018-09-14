import os
import sys
from Node import Node
from readGrouper import reader

def edit(data):
	file = "/Users/stuartki/Documents/connector/" + topic + ".txt"
	start = ""
	
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
				
		
	return data
				