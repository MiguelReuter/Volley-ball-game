# encoding : UTF-8

import pygame as pg

import Engine
from Settings.general_settings import BKGND_TRANSPARENCY_COLOR, DEBUG_TEXT_COLOR


class DebugText(pg.sprite.GroupSingle):
	"""
	Class for debug text displaying on game window.
	"""
	
	def __init__(self):
		pg.sprite.GroupSingle.__init__(self)
		self.content = {"test": 45,
		                "other test": "Hello"}
		self.font = pg.font.Font("../assets/font/PressStart2P.ttf", 8)
		self.image = None
		self.rect_list = []
	
	def create_image(self, size=(0, 0)):
		"""
		Create image and set colorkey.

		:param tuple(int, int) size: size of image to create
		:return: None
		"""
		self.image = pg.Surface(size)
		self.image.fill(BKGND_TRANSPARENCY_COLOR)
		self.image.set_colorkey(BKGND_TRANSPARENCY_COLOR)
	
	def update(self):
		"""
		Update image and list of rects to redraw.

		This method is not really optimised. For each frame, the previous rects are cleared and current rects are
		redraw, even nothing has changed.

		:return: None
		"""
		for r in self.rect_list:
			self.image.fill(BKGND_TRANSPARENCY_COLOR, r)
		
		self.rect_list = []
		x = 20
		y = 20
		key_max_length = 10
		
		# update content
		self.content["ticks"] = Engine.game_engine.GameEngine.get_instance().get_running_ticks()
		
		# for each key in self.content dict, a new line
		for k in self.content:
			k_str = k.ljust(key_max_length)
			text_surface = self.font.render(k_str + ": " + str(self.content[k]), 0, DEBUG_TEXT_COLOR)
			self.rect_list += [pg.Rect((x, y), text_surface.get_size())]
			self.image.blit(text_surface, (x, y))
			y += int(1.5 * self.font.get_height())
