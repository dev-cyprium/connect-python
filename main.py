import pygame
from game.game_object import Grid, ClickableTile
from game.event_dispatcher import EventDispatcher

class Game(object):
	
	WIDTH  = 800
	HEIGHT = 600
	
	def __init__(self):
		self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
		self.done = False
		self.clock = pygame.time.Clock()
		self.game_objects = []
		self.dispatcher = EventDispatcher()
		
		self.grid = Grid(400 - 125, 300 - 125, 5)
		
		self.clickable = ClickableTile(400 - 135, 300 - 125)
		self.clickable1 = ClickableTile(400 - 25, 300 - 80)
		self.clickable2 = ClickableTile(400 - 25, 300 - 15)
		self.clickable3 = ClickableTile(0, 300 - 125)
		
		# Add event listener to clickable tile
		self.dispatcher.subscribe(self.clickable)
		self.dispatcher.subscribe(self.clickable1)
		self.dispatcher.subscribe(self.clickable2)
		self.dispatcher.subscribe(self.clickable3)
		
		self.game_objects.append(self.grid)
		self.game_objects.append(self.clickable)
		self.game_objects.append(self.clickable1)
		self.game_objects.append(self.clickable2)
		self.game_objects.append(self.clickable3)
		
	def run(self):
		while not self.done:
			for event in pygame.event.get():
				self.dispatcher.dispatch(event)
				if event.type == pygame.QUIT:
					self.done = True
			# Game update logic
			self.clickable.update()
			self.clickable1.update()
			self.clickable2.update()
			self.clickable3.update()
			
			# Game render the screen		
			self.screen.fill((0, 0, 0))
			for obj in self.game_objects:
				obj.render(self.screen)
			self.clock.tick(60)
			
			pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	g = Game()
	g.run()