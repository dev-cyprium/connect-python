import pygame
from game.scene import GameSceneManager, GameScene, MenuScene

class Game(object):
	
	WIDTH  = 800
	HEIGHT = 600
	
	def __init__(self):
		self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
		self.done = False
		self.clock = pygame.time.Clock()
		self.scene_manager = GameSceneManager()
		self.scene_manager.set_default_scene( MenuScene(self.scene_manager) )
		
	def run(self):
		while not self.done:
			active_scene = self.scene_manager.active_scene()
			for event in pygame.event.get():
				active_scene.dispatch_event(event)
				if event.type == pygame.QUIT:
					self.done = True
			active_scene.update()		
			self.screen.fill((0, 0, 0))
			active_scene.render(self.screen)
			self.clock.tick(60)
			pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	g = Game()
	g.run()