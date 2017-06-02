from game.utilities import Stack
from random import randrange
from game.game_object import Grid, Figure, Button
from game.event_dispatcher import EventDispatcher
from game.figure_parser import FigureParser
import pygame

class GameSceneManager(object):
	def __init__(self, default_scene):
		self._scene_stack = Stack()
		self._scene_stack.push(default_scene)
		
	def switch_scene(self, scene):
		self._scene_stack.push(scene)
		
	def active_scene(self):
		return self._scene_stack.peek()

'''
	Scene responsible for the main game menu
'''
class MenuScene(object):
	def __init__(self):
		self.font = pygame.font.SysFont('arial', 64)
		self.button_font = pygame.font.SysFont('arial', 20)
		self.dispatcher = EventDispatcher()
		
		self.play_button = Button(340, 240, self.button_font, 'Play', self)
		self.exit_button = Button(340, 300, self.button_font, 'Exit', self)
		
		self.dispatcher.subscribe( self.play_button )
		self.dispatcher.subscribe( self.exit_button )
		
	def dispatch_event(self, event):
		self.dispatcher.dispatch(event)
		
	def render(self, surface):
		label = self.font.render('Connect', 1, (255,255,255))
		surface.blit(label, (280, 120))
		self.play_button.render(surface)
		self.exit_button.render(surface)
				
	def update(self):
		pass

'''
Scene responsible for the gameplay
'''			
class GameScene(object):
	def __init__(self):
		self.dispatcher = EventDispatcher()
		self.game_objects = []
		self.grid = Grid(400 - 125, 300 - 125, 5, self)
		self.dispatcher.subscribe(self.grid)
		self.game_objects.append(self.grid)
		
		# Load figures
		self.figures = []
		parser = FigureParser()
		for figure in parser.parse_figure_file():
			f = Figure(randrange(50, 600), randrange(50, 400), figure['vertecies'], self)
			self.figures.append( f )
			self.dispatcher.subscribe( f )
			self.game_objects.append( f )
		
		# Load the music
		# pygame.mixer.music.load('./res/theme.mp3')
		# pygame.mixer.music.set_volume(0.1)
		# pygame.mixer.music.play(-1, 0.0)
	def dispatch_event(self, event):
		self.dispatcher.dispatch(event)
		
	def render(self, surface):
		for obj in self.game_objects:
			obj.render(surface)
		
	def update(self):
		for obj in self.game_objects:
			obj.update()
		
	