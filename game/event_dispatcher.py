import pygame
'''
Event listener class used to dispatch click events to subscribed game objects
'''
class EventDispatcher(object):
	def __init__(self):
		self.listeners = []
		
	def dispatch(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for listener in self.listeners:
				listener.on_click(event)
				
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			for listener in self.listeners:
				listener.on_release(event)
				
	def subscribe(self, obj):
		self.listeners.append(obj)