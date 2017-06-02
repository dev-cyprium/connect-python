from game.utilities import Stack

class GameSceneManager(object):
	def __init__(self, default_scene):
		self._scene_stack = Stack()
		self._scene_stack.push(default_scene)
		
	def switch_scene(self, scene):
		self._scene_stack.push(scene)
		
	def active_scene(self):
		self._scene_stack.peek()
			
class GameScene(object):
	def __init__(self):
		pass
		
	def render(self, surface):
		pass
		
	def update(self):
		pass
		
	