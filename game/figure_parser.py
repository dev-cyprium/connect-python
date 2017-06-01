import json

class FigureParser(object):
	def __init__(self):
		self.file_path = '../res/layouts.json'
		
	def parse_figure_file(self):
		with open(self.file_path) as data_file:
			data = json.load(data_file)
			return data['layout1']['figures']