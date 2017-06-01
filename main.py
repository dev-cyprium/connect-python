import pygame
from game.game_object import Grid, Figure
from game.event_dispatcher import EventDispatcher
from game.figure_parser import FigureParser

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
		self.game_objects.append(self.grid)
		
		# Load figures
		self.figures = []
		parser = FigureParser()
		for figure in parser.parse_figure_file():
			f = Figure(0, 0, figure['vertecies'])
			self.figures.append( f )
			self.dispatcher.subscribe( f )
			self.game_objects.append( f )

		
		
	def run(self):
		while not self.done:
			# Event listening
			for event in pygame.event.get():
				self.dispatcher.dispatch(event)
				if event.type == pygame.QUIT:
					self.done = True
			
			# Game update logic
			for obj in self.game_objects:
				obj.update()
			
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