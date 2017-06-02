import pygame
from random import randrange

class GameObject(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def render(self, surface):
		pass
	
	def update(self):
		pass
		
class Grid(GameObject):
	def __init__(self, x, y, size):
		super().__init__(x, y)
		self.tiles = [[BlankTile(self.x + x * BlankTile.SIZE, self.y + y * BlankTile.SIZE) for x in range(size)] for y in range(size)]
		
	def render(self, surface):
		for tiles in self.tiles:
			for tile in tiles:
				tile.render(surface)
				
	def update(self):
		if Figure.active_figure is not None:
			Figure.active_figure.switch_color( (255, 255, 255) )
		
class BlankTile(GameObject):
	SIZE = 50
	
	def __init__(self, x, y):
		super().__init__(x, y)
		self.width  = BlankTile.SIZE
		self.height = BlankTile.SIZE
		self.color = (107, 107, 107)
		
	def render(self, surface):
		pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
		pygame.draw.rect(surface, (0,0,0), pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 4))
		
class ClickableTile(GameObject):
	SIZE = 50
	
	def __init__(self, x, y, color):
		super().__init__(x, y)
		self.width = ClickableTile.SIZE
		self.height = ClickableTile.SIZE
		self.color = color
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		
	def render(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
		
class Figure(GameObject):
	
	active_figure = None
	
	def __init__(self, x, y, vertecies):
		super().__init__(x, y)
		self.color = (randrange(0,256), randrange(0,256), randrange(0,256))
		self.tiles = []
		
		for vertex in vertecies:
			self.tiles.append(ClickableTile(self.x + vertex[0] * ClickableTile.SIZE, self.y + vertex[1] * ClickableTile.SIZE, self.color))
					
		self.dragging = False
		self.mouse_position = None
		
	def switch_color(self, color):
		for tile in self.tiles:
			tile.color = color
		
	def update(self):
		if(self.dragging):
			current_position = pygame.mouse.get_pos()
			move_x = self.mouse_position[0] - current_position[0]
			move_y = self.mouse_position[1] - current_position[1]
			for tile in self.tiles:
				tile.x -= move_x
				tile.y -= move_y
				tile.rect = pygame.Rect(tile.x, tile.y, tile.width, tile.height)
		self.mouse_position = pygame.mouse.get_pos()
			
		
	def render(self, surface):
		for tile in self.tiles:
			tile.render(surface)
	
	def on_click(self, event):
		print(repr(self.tiles))
		Figure.active_figure = self
		for tile in self.tiles:
			if(tile.rect.collidepoint(event.pos)):
				self.dragging = True
				
	def on_release(self, event):
		Figure.active_figure = None
		self.dragging = False