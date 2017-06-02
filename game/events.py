class FigureReleaseEvent(object):
	# Big number to not conflict with other events
	FIGURERELEASE = 9000
	
	def __init__(self, figure):
		self.type = FigureReleaseEvent.FIGURERELEASE
		self.figure = figure