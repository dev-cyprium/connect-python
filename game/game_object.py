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
		self.placers = []
		
	def render(self, surface):
		for tiles in self.tiles:
			for tile in tiles:
				tile.render(surface)
	
	def on_figure_release(self, figure):
		if len(self.placers) == 0:
			return
		figure.move_to(self.placers[0].x, self.placers[0].y)
				
	def update(self):
		for tiles in self.tiles:
			for tile in tiles:
				tile.active = False
				self.placers = []
		
		if Figure.active_figure is not None:	
			figure = Figure.active_figure
			for figure_tile in figure.tiles:
				candidates = []
				for tiles in self.tiles:
					for tile in tiles:
						info = {}
						if(tile.rect.colliderect(figure_tile.rect)):
							clip_rect = tile.rect.clip(figure_tile.rect)
							info['tile'] = tile
							info['clip_area'] = clip_rect.width * clip_rect.height
							candidates.append(info)
				if len(candidates) == 0:
					continue
				highlited = max(candidates, key=lambda d: d['clip_area'])
				highlited['tile'].active = True
				self.placers.append(highlited['tile'])
				
class BlankTile(GameObject):
	SIZE = 50
	
	def __init__(self, x, y, scene):
		super().__init__(x, y, scene)
		self.width  = BlankTile.SIZE
		self.height = BlankTile.SIZE
		self.color = (107, 107, 107)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.active = False
		self.hover_color = (200, 200, 200)
		self.normal_color = (0, 0, 0)
			
	def render(self, surface):
		if self.active: 
			self.normal_color = self.hover_color
		else:
			self.normal_color = (0,0,0)  
		pygame.draw.rect(surface, self.color, self.rect)
		pygame.draw.rect(surface, self.normal_color, pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 4))
		
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
		self.vertecies = vertecies
		for vertex in vertecies:
			self.tiles.append(ClickableTile(self.x + vertex[0] * ClickableTile.SIZE, self.y + vertex[1] * ClickableTile.SIZE, self.color, scene))
		self.x = self.x + vertecies[0][0] * ClickableTile.SIZE
		self.y = self.y + vertecies[0][1] * ClickableTile.SIZE
		self.dragging = False
		self.mouse_position = None
		
	def switch_color(self, color):
		for tile in self.tiles:
			tile.color = color
	
	def revert_color(self):
		for tile in self.tiles:
			tile.color = self.original_color
	
	def move_to(self, x, y):
		self.x = x - self.vertecies[0][0] * ClickableTile.SIZE
		self.y = y - self.vertecies[0][1] * ClickableTile.SIZE
		for idx, tile in enumerate(self.tiles):
			tile.x = self.x + self.vertecies[idx][0] * ClickableTile.SIZE
			tile.y = self.y + self.vertecies[idx][1] * ClickableTile.SIZE	
		
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