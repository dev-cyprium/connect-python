import pygame
from game.events import FigureReleaseEvent
'''
Event listener class used to dispatch click events to subscribed game objects
'''
class EventDispatcher(object):
	def __init__(self):
		self.listeners = []
		
	def dispatch(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for listener in self.listeners:
				if hasattr(listener, 'on_click'):
					listener.on_click(event)
				
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			for listener in self.listeners:
				if hasattr(listener, 'on_release'):
					listener.on_release(event)
		
		if event.type == FigureReleaseEvent.FIGURERELEASE:
			for listener in self.listeners:
				if hasattr(listener, 'on_figure_release'):
					listener.on_figure_release(event.figure)
				
	def subscribe(self, obj):
		self.listeners.append(obj)
		
	def clear_queue(self):
		self.listeners = []