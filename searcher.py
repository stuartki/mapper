
import os
import sys
from Node import Node
	
def pastNode(content, data):
	pastNodes = []
	words = word_tokenize(content)


	stop_words = set(stopwords.words('english'))

	fs = [w for w in words if not w.lower() in stop_words]
	
	f = list(set(fs))

	for x in data:
		if isinstance(x, int):
			continue
		if x.title in f:
			pastNodes.append(x.id)
	return pastNodes

def ngram(input, n):
	input = input.split(' ')
	output = []
	for i in range(len(input)-n+1):
		f = ""
		for s in input[i:i+n]:
			f += s + ' '
			
		f = f[:-1]
		output.append(f)
	return output

def searcher(word, data):
	def ngram(input, n):
		input = input.split(' ')
		output = []
		for i in range(len(input)-n+1):
			f = ""
			for s in input[i:i+n]:
				f += s + ' '
			
			f = f[:-1]
			output.append(f)
		return output
	word = word.lower()
	n =  len(word.split(' '))
	returnArray = []
	
	for node in data:
		if isinstance(node, int):
			continue
		for w in ngram(node.title, n):
			if word == w.lower():
				returnArray.append(node)
				break
		
			
		
	return returnArray
