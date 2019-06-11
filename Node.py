import numpy

class Node(object):
	def __init__(self, title, type, description, keywords, past, future, related, id):
		self.title = title
		self.type = type
		self.description = description
		self.keywords = keywords
		self.past = past
		self.future = future
		self.id = id
		self.related = related
	def flashback(self, back):
		self.past.append(back)
	def flashforward(self, forward):
		self.future.append(forward)
	def relate(self, relate):
		self.related.append(relate)
	def printNode(self):
		print(self.id)
		print(self.title)
		print(self.type)
		print(self.past)
		print(self.future)
		print(self.related)
		print(self.keywords)
		print(self.description)
	
	