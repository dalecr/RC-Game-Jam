# circularLinkedList.py
# A limited implementation of a circular singly-linked list 
# Created 2/24/2017 by Connor Dale

class Node:
	# A Node class that holds data and a pointer to the next node in the linked list

	def __init__(self,data,next):
		'''
		Creates a Node object
		Inputs:
			data ------ the information stored in the node
			next ------ the next node in the list
		Outputs:
			None
		'''
		self.data = data
		self.next = next
		__slots__ = [self.data, self.next]


class CircularLinkedList:
	# A circular linked list class that stores data as a chain of Node objects
	
	def __init__(self):
		'''
		Creates a CircularLinkedList object
		Inputs:
			None
		Outputs:
			None
		'''
		self.last = None  # the last node in the list
		self.current = None # the current player


	def append(self,data):
		'''
		Adds a node with the given data to the end of the list
		Inputs:
			data --------- the information to be stored
		Outputs:
			None
		'''
		new_node = Node(data,None)  # node to be added

		if self.is_empty():
			self.last = new_node
			new_node.next = new_node
		else:
			new_node.next = self.last.next  # new node links to first node
			self.last.next = new_node  # previous last node links to new node
			self.last = new_node  # new node gets last-node pointer 


	def set_current(self,data=None):
		'''
		Searches the list for a node containing the specified value, then 
		sets the current player marker
		Inputs:
			data --------- the value in the list that is searched for
		Outputs:
			None
		'''
		if not self.is_empty():
			if data == None:
				self.current = self.last
				return
			marker = self.last
			while True:
				marker = marker.next
				if marker.data == data:
					self.current = marker
				if marker == self.last:
					return


	def update_current(self):
		'''
		Sets the current player marker to the next in the list
		Inputs:
			None
		Outputs:
			None
		'''
		if self.current != None:
			self.current = self.current.next


	def is_empty(self):
			'''
			Checks whether there is a value assigned to self.last
			to determine whether there are any elements in the list
			Inputs:
				None
			Outputs:
				True ------ if list is empty
				False ----- if it isn't
			'''
			if self.last == None:
				return True
			return False