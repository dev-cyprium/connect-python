class FigureReleaseEvent(object):
	# Big number to not conflict with other events
	FIGURERELEASE = 9000
	
	def __init__(self):
		self.type = FigureReleaseEvent.FIGURERELEASE