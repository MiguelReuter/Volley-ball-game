# encoding : UTF-8

import pygame as pg

DEBUG_3D_COLOR = (0, 200, 0)


class Debug3D(pg.sprite.GroupSingle):
	"""
	Class for 3D shapes displaying on game window.
	"""
	
	def __init__(self):
		pg.sprite.GroupSingle.__init__(self)
		self.image = None
		self.rect_list = []
		self.prev_rect_list = []
	
	def create_image(self, size=(0, 0)):
		self.image = pg.Surface(size)
		self.image.fill(DEBUG_3D_COLOR)
		self.image.set_colorkey(DEBUG_3D_COLOR)
	
	def update(self, objects):
		self.prev_rect_list = self.rect_list
		self.rect_list = []
		self.image.fill(DEBUG_3D_COLOR)
		
		for obj in objects:
			rects = obj.draw()
			if rects is not None:
				self.rect_list += rects
				