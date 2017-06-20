from random import randrange
from game.game_object import Grid, Figure, Button, SoundButton, ResetButton
from game.event_dispatcher import EventDispatcher
from game.figure_parser import FigureParser
import pygame
import sys
import math
		
class GameSceneManager(object):
	def __init__(self):
		self._scene_stack = []
		
	def switch_scene(self, scene):
		self._scene_stack.append(scene)
		
	def active_scene(self):
		return self._scene_stack[-1]
		
	def set_default_scene(self, scene):
		self._scene_stack.append(scene)
		
	def clear_queue(self):
		self._scene_stack = []

'''
	Scene responsible for the main game menu
'''
class MenuScene(object):
	def __init__(self, manager):
		self.font = pygame.font.SysFont('arial', 64)
		self.button_font = pygame.font.SysFont('arial', 20)
		self.dispatcher = EventDispatcher()
		
		self.play_button = Button(340, 240, self.button_font, 'Play', self, lambda: manager.switch_scene( GameScene(manager) ) )
		self.exit_button = Button(340, 300, self.button_font, 'Exit', self, lambda: sys.exit() )
		
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
	def __init__(self, manager, music_paused=False):
		self.dispatcher = EventDispatcher()
		self.game_objects = []
		self.grid = Grid(400 - 125, 300 - 125, 5, self)
		self.dispatcher.subscribe(self.grid)
		self.manager = manager
		self.game_objects.append(self.grid)
		self.won = False
		self.font = pygame.font.SysFont('arial', 20)
		self.reset_button = Button(350, 300, self.font, "Reset", self, self.reset )
		self.sound_button = SoundButton(10, 10, self, self.toggle_music )
		self.game_reset   = ResetButton(80, 10, self, self.reset )
		
		self.dispatcher.subscribe(self.reset_button)
		self.dispatcher.subscribe(self.sound_button)
		self.dispatcher.subscribe(self.game_reset)
		
		# Load figures
		self.figures = []
		parser = FigureParser()
		radius = 230
		angle = 0
		for figure in parser.parse_figure_file():
			x = figure["x"]
			y = figure["y"]
			angle += math.pi / 4
			f = Figure(x, y, figure['vertecies'], figure['width'], figure['height'], self, figure['offset_x'])
			self.figures.append( f )
			self.dispatcher.subscribe( f )
			self.game_objects.append( f )
		
		# Load the music
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.load('./res/theme.mp3')
			pygame.mixer.music.set_volume(0.1)
			pygame.mixer.music.play(-1, 0.0)
			self.music_on = True
		else:
			if music_paused:
				self.music_on = True
			else:
				self.music_on = False
			self.sound_button.set_state(self.music_on)
		
	def dispatch_event(self, event):
		self.dispatcher.dispatch(event)
		
	def render(self, surface):
		if Figure.active_figure is not None:
			figure = Figure.active_figure
			for obj in self.game_objects:
				if obj is not figure:	
					obj.render(surface)
			figure.render(surface)
		else:
			for obj in self.game_objects:
				obj.render(surface)
		
		self.sound_button.render(surface)
		self.game_reset.render(surface)
		
		if self.won:
			pygame.draw.rect(surface, (255,255,255), pygame.Rect(400 - 100, 300 - 50, 200, 100))
			pygame.draw.rect(surface, (0,0,0), pygame.Rect(400 - 99, 300 - 49, 198, 98))
			label = self.font.render("Congratulations", 1, (255, 255, 255))
			surface.blit(label, (330, 260))
			self.reset_button.render(surface)
			
	def update(self):
		for obj in self.game_objects:
			obj.update()
	
	def win(self):
		self.won = True
		self.dispatcher.clear_queue()
		self.dispatcher.subscribe(self.reset_button)
	
	def reset(self):
		self.dispatcher.clear_queue()
		self.manager.clear_queue()
		new_scene = GameScene(self.manager, self.music_on)
		self.manager.set_default_scene(new_scene)
		
	def toggle_music(self):
		if self.music_on:
			self.music_on = False
			pygame.mixer.music.pause()
		else:
			self.music_on = True
			pygame.mixer.music.unpause()