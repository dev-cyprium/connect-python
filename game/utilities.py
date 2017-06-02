'''
Custom data-strcture representing a stack
'''
class Stack(object):
	def __init__(self):
		self._arr = []
		
	def push(self, obj):
		self._arr.append(obj)
		
	def pop(self, obj):
		return self._arr.pop()
		
	def peek(self):
		return self._arr[-1]