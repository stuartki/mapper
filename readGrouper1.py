
import os
import sys
from Node import Node
import json
	
def reader(topic):
	file = "/Users/stuartki/Documents/connector/" + topic + ".json"

	tempData = []

	with open(file, "r") as current_file:
		tempData = json.load(current_file)


	max = len(tempData)
	if max == 0:
		max += 1


	data = [max]


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

		count = 0
	
	
		#ID = 0, PAST = 1, FUTURE = 2, KEYWORDS = 3, DESCRIPTION = 4, 
	
		id = line["id"]
		past = line["past"]
		title = line["title"]
		type = line["type"]
		future = line["future"]
		description = line["description"]
		keywords = line["keywords"]
		related = line["related"]
		
	
		current_node = Node(title, type, description, keywords, past, future, related, id)
		data.append(current_node)
		
	
	return data