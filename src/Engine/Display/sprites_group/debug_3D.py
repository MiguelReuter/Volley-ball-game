# encoding : UTF-8

import pygame as pg

from Settings.general_settings import BKGND_TRANSPARENCY_COLOR


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
		"""
		Create image and set colorkey.
		
		:param tuple(int, int) size: size of image to create
		:return: None
		"""
		self.image = pg.Surface(size)
		self.image.fill(BKGND_TRANSPARENCY_COLOR)
		self.image.set_colorkey(BKGND_TRANSPARENCY_COLOR)
	
	def update(self, objects):
		"""
		Update image and list of rects to redraw.
		
		This method is not really optimised. For each frame, the previous rects are cleared and current rects are
		redraw, even nothing has changed.
		
		:param list() objects: list of objects with a draw_debug() method whichreturn None or a list of rects
		:return: None
		"""
		self.prev_rect_list = self.rect_list
		self.rect_list = []
		
		# clear previous rects
		for r in self.prev_rect_list:
			self.image.fill(BKGND_TRANSPARENCY_COLOR, r)
		
		# draw objects
		for obj in objects:
			rects = obj.draw_debug()
			if rects is not None:
				self.rect_list += rects
				