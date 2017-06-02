import pygame
from random import randrange
from game.events import FigureReleaseEvent

class GameObject(object):
	def __init__(self, x, y, scene):
		self.x = x
		self.y = y
		self.scene = scene
		
	def render(self, surface):
		pass
	
	def update(self):
		pass
		
class Grid(GameObject):
	def __init__(self, x, y, size, scene):
		super().__init__(x, y, scene)
		self.tiles = [[BlankTile(self.x + x * BlankTile.SIZE, self.y + y * BlankTile.SIZE, scene) for x in range(size)] for y in range(size)]
		
	def render(self, surface):
		for tiles in self.tiles:
			for tile in tiles:
				tile.render(surface)
				
	def on_figure_release(self, figure):
		for tiles in self.tiles:
			for tile in tiles:
				for figure_tile in figure.tiles:
					if(figure_tile.rect.colliderect(tile)):
						figure_tile.x = tile.x
						figure_tile.y = tile.y
				
		
class BlankTile(GameObject):
	SIZE = 50
	
	def __init__(self, x, y, scene):
		super().__init__(x, y, scene)
		self.width  = BlankTile.SIZE
		self.height = BlankTile.SIZE
		self.color = (107, 107, 107)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
			
	def render(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
		pygame.draw.rect(surface, (0,0,0), pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 4))
		
class ClickableTile(GameObject):
	SIZE = 50
	
	def __init__(self, x, y, color, scene):
		super().__init__(x, y, scene)
		self.width = ClickableTile.SIZE
		self.height = ClickableTile.SIZE
		self.color = color
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		
	def render(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
		
class Figure(GameObject):
	
	active_figure = None
	
	def __init__(self, x, y, vertecies, scene):
		super().__init__(x, y, scene)
		self.color = (randrange(0,256), randrange(0,256), randrange(0,256))
		self.original_color = self.color
		self.tiles = []
		
		for vertex in vertecies:
			self.tiles.append(ClickableTile(self.x + vertex[0] * ClickableTile.SIZE, self.y + vertex[1] * ClickableTile.SIZE, self.color, scene))
					
		self.dragging = False
		self.mouse_position = None
		
	def switch_color(self, color):
		for tile in self.tiles:
			tile.color = color
	
	def revert_color(self):
		for tile in self.tiles:
			tile.color = self.original_color
		
	def update(self):
		if(self.dragging):
			current_position = pygame.mouse.get_pos()
			move_x = self.mouse_position[0] - current_position[0]
			move_y = self.mouse_position[1] - current_position[1]
			for tile in self.tiles:
				tile.x -= move_x
				tile.y -= move_y
			self.x = self.tiles[0].x
			self.y = self.tiles[0].y
		self.mouse_position = pygame.mouse.get_pos()
		
		for tile in self.tiles:
			tile.rect = pygame.Rect(tile.x, tile.y, tile.width, tile.height)
		
		if Figure.active_figure is not None:
			Figure.active_figure.switch_color( (255, 255, 255) )	
		
	def render(self, surface):
		for tile in self.tiles:
			tile.render(surface)
	
	def on_click(self, event):
		for tile in self.tiles:
			if(tile.rect.collidepoint(event.pos)):
				self.dragging = True
				Figure.active_figure = self
				
	def on_release(self, event):
		figure = Figure.active_figure
		if self is not figure:
			return
		self.scene.dispatcher.dispatch( FigureReleaseEvent(figure) )
		Figure.active_figure = None
		figure.dragging = False
		figure.revert_color()