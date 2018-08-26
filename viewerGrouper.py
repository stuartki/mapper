import os
import sys
from Node import Node
from readGrouper import reader
	
	
def viewer(topic):
	data = reader(topic)
	current_node = data[1]
	
	start = ""
	
	while start != "end":
		print current_node.title
		print current_node.description
		
		start = raw_input("")
		if start == "end":
			continue
			
		if start == ">":
			current = ""
			futureArray = current_node.future
			for n in futureArray:
				if n == '':
					continue
				n = int(n)
				print data[n].id
				print data[n].title
				print data[n].description
			while current != "end":
				current = raw_input("")
				if current == "end":
					continue
				point = int(current)
				current_node = data[point]
			
		if start == "<":
			curr = ""
			pastArray = current_node.past
			for n in pastArray:
				if n == '':
					continue
				n = int(n)
				print data[n].id
				print data[n].title
				print data[n].description
				
			while curr != "end":
				curr = raw_input("")
				if curr == "end":
					continue
				point = int(curr)
				current_node = data[point]
				
		if start == "r":
			curr = ""
			rArray = current_node.related
			for n in rArray:
				if n == '':
					continue
				n = int(n)
				print data[n].id
				print data[n].title
				print data[n].description
				
			while curr != "end":
				curr = raw_input("")
				if curr == "end":
					continue
				point = int(curr)
				current_node = data[point]
				
		if start == "all":
			curr = ""
			rArray = current_node.related
			for n in rArray:
				if n == '':
					continue
				n = int(n)
				print data[n].id
				print data[n].title
				print data[n].description
				
			while curr != "end":
				curr = raw_input("")
				if curr == "end":
					continue
				point = int(curr)
				current_node = data[point]
		
		
		
		