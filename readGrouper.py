
import os
import sys
from Node import Node
	
def reader(topic):
	file = "/Users/stuartki/Documents/connector/" + topic + ".txt"

	tempData = []

	with open(file, "r") as current_file:
		tempData = current_file.readlines()
		max = len(tempData)



	if max == 0:
		max += 1


	data = []


	#turning the lines into nodes
	id = 0
	past = []
	title = ""
	type = ""
	future = []
	description = ""
	keywords = []
	related = []

	for line in tempData:
	
		if id == 0:
			num = int(line)
			data.append(num)
			id += 1
			continue
		

	
		element = line.split(',')

		count = 0
	
	
		#ID = 0, PAST = 1, FUTURE = 2, KEYWORDS = 3, DESCRIPTION = 4, 
	
		for e in element:
			if count == 0:
				id = e
			if count == 1:
				title = e
			if count == 2:
				type = e
			if count == 3:
				past = e.split('|')
			if count == 4:
				future = e.split('|')
			if count == 5:
				related = e.split('|')
			if count == 6:
				keywords = e.split('|')
			if count == 7:
				description = e
			count+=1
		
	
		current_node = Node(title, type, description, keywords, past, future, related, id)
		data.append(current_node)
		
	
	return data