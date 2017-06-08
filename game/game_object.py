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
		
class Button(GameObject):
	def __init__(self, x, y, font, text, scene, action):
		super().__init__(x, y, scene)
		self.font = font
		self.width = 100
		self.height = 30
		self.text = text
		if font is not None:
			self.font_width = font.size(text)[0]
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.action = action
		
	def render(self, surface):
		pygame.draw.rect(surface, (255, 255, 255), self.rect)
		label = self.font.render(self.text, 1, (0, 0, 0))
		surface.blit(label, (self.x + (self.width / 2) - self.font_width / 2, self.y + 4))	
	
	def on_click(self, event):
		if(self.rect.collidepoint(event.pos)):	
			self.action()
			
class ResetButton(Button):
	def __init__(self, x, y, scene, action):
		super().__init__(x, y, None, None, scene, action)
		self.image = pygame.image.load('./res/restart.png')
		self.circle_position = (self.x + 30, self.y + 30)
		self.radius = 30
		
	def render(self, surface):
		surface.blit(self.image, (self.x, self.y))	
		
	def on_click(self, event):
		mx = event.pos[0]
		my = event.pos[1]
		cx = self.x + 30
		cy = self.y + 30
		if (mx - cx)**2 + (my - cy)**2 < self.radius**2:
			self.action()
			
class SoundButton(Button):
	
	MUTED = 1
	UNMUTED = 0
	
	def __init__(self, x, y, scene, action):
		super().__init__(x, y, None, None, scene, action)
		self.mute_image   = pygame.image.load('./res/mute.png')
		self.unmute_image = pygame.image.load('./res/unmute.png')
		self.state = SoundButton.UNMUTED
		self.circle_position = (self.x + 30, self.y + 30)
		self.radius = 30
		
	def render(self, surface):
		if self.state == SoundButton.MUTED:
			pic = self.mute_image
		else:
			pic = self.unmute_image
		
		surface.blit(pic, (self.x, self.y))
	
	def set_state(self, state):
		if state:
			self.state = SoundButton.UNMUTED
		else:
			self.state = SoundButton.MUTED
		
	
	def on_click(self, event):
		mx = event.pos[0]
		my = event.pos[1]
		cx = self.x + 30
		cy = self.y + 30
		if (mx - cx)**2 + (my - cy)**2 < self.radius**2:
			if self.state == SoundButton.UNMUTED:
				self.state = SoundButton.MUTED
			else:
				self.state = SoundButton.UNMUTED
			
			self.action()
		
			
class Grid(GameObject):
	def __init__(self, x, y, size, scene):
		super().__init__(x, y, scene)
		self.tiles = [[BlankTile(self.x + x * BlankTile.SIZE, self.y + y * BlankTile.SIZE, scene) for x in range(size)] for y in range(size)]
		self.placers = []
		
	def render(self, surface):
		for tiles in self.tiles:
			for tile in tiles:
				tile.render(surface)
	
	def check_collision_with_others(self, figure):
		colided = False
		other_figure_tiles = []
		for obj in self.scene.game_objects:
			if obj.__class__.__name__ == 'Figure':
				if obj == figure: continue
				other_figure_tiles.extend(map( lambda item: item.rect, obj.tiles) )
				
		for my_rect in map(lambda item: item.rect, figure.tiles):
			for other_rect in other_figure_tiles:
				if my_rect.colliderect(other_rect):
					colided = True
					break  
		return colided
	
	def on_figure_release(self, figure):
		if len(self.placers) == 0:
			if self.check_collision_with_others(figure):
				old_x = figure.pick_location[0]
				old_y = figure.pick_location[1]
				figure.move_to(old_x, old_y)
			return
						
		ocupied = False
		for placer in self.placers:
			if placer.ocupied:
				ocupied = True
				break
					
		if not ocupied and len(self.placers) == len(figure.tiles):
			figure.move_to(self.placers[0].x, self.placers[0].y)
			for placer in self.placers:
				placer.ocupied = True
			figure.ocupied_tiles = self.placers
		else:
			old_x = figure.pick_location[0]
			old_y = figure.pick_location[1]
			figure.move_to(old_x, old_y)
			
			
		normal = 0
		ocupied = 0
		for tiles in self.tiles:
			for tile in tiles:
				if tile.ocupied: 
					ocupied += 1
				normal += 1
		
		if normal == ocupied:
			self.scene.win()
				
	def update(self):
		print("Placers length: {}".format(len(self.placers)))
		active_tiles = [j for i in self.tiles for j in i if j.active]
		print("Active tiles count: {}".format(len(active_tiles)))
		
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
				if not highlited['tile'].active:
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
		self.ocupied = False
			
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
	
	def __init__(self, x, y, vertecies, width, height, scene):
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
		self.width = width * ClickableTile.SIZE
		self.height = height * ClickableTile.SIZE
		self.pick_location = (self.x, self.y)
		self.ocupied_tiles = None
		
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
			self.x -= move_x
			self.y -= move_y
			if self.x < 0:
				self.x = 0
			if self.y < 0:
				self.y = 0
			if self.x + self.width > 800:
				self.x = 800 - self.width
			if self.y + self.height > 600:
				self.y = 600 - self.height
			self.move_to(self.x, self.y)
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
		if Figure.active_figure is None:
			for tile in self.tiles:
				if(tile.rect.collidepoint(event.pos)):
					if self.ocupied_tiles is not None:
						for tile in self.ocupied_tiles:
							tile.ocupied = False
					self.ocupied_tiles = None
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