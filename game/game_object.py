import pygame

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
	
	def __init__(self, x, y):
		super().__init__(x, y)
		self.width = ClickableTile.SIZE
		self.height = ClickableTile.SIZE
		self.color = (255, 255, 0)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.dragging = False
		self.mouse_position = None
		
	def render(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)
	
	def update(self):
		if(self.dragging):
			current_position = pygame.mouse.get_pos()
			move_x = self.mouse_position[0] - current_position[0]
			move_y = self.mouse_position[1] - current_position[1]
			self.x -= move_x
			self.y -= move_y
			self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.mouse_position = pygame.mouse.get_pos()
	
	def on_click(self, event):
		if(self.rect.collidepoint(event.pos)):
			self.dragging = True
		
	def on_release(self, event):
		self.dragging = False