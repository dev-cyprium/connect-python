from game.utilities import Stack
from random import randrange
from game.game_object import Grid, Figure
from game.event_dispatcher import EventDispatcher
from game.figure_parser import FigureParser

class GameSceneManager(object):
	def __init__(self, default_scene):
		self._scene_stack = Stack()
		self._scene_stack.push(default_scene)
		
	def switch_scene(self, scene):
		self._scene_stack.push(scene)
		
	def active_scene(self):
		return self._scene_stack.peek()
			
class GameScene(object):
	def __init__(self):
		self.dispatcher = EventDispatcher()
		self.game_objects = []
		self.grid = Grid(400 - 125, 300 - 125, 5)
		self.game_objects.append(self.grid)
		
		# Load figures
		self.figures = []
		parser = FigureParser()
		for figure in parser.parse_figure_file():
			f = Figure(randrange(50, 600), randrange(50, 400), figure['vertecies'])
			self.figures.append( f )
			self.dispatcher.subscribe( f )
			self.game_objects.append( f )
	
	def dispatch_event(self, event):
		pass
		
	def render(self, surface):
		for obj in self.game_objects:
			obj.render(surface)
		
	def update(self):
		for obj in self.game_objects:
			obj.update()
		
	