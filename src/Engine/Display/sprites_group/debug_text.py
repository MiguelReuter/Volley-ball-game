# encoding : UTF-8

import pygame as pg
import Engine

DEBUG_TEXT_COLOR = (200, 200, 0)

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
		self.image = pg.Surface(size)
		self.image.fill(DEBUG_TEXT_COLOR)
		self.image.set_colorkey(DEBUG_TEXT_COLOR)
	
	def update(self):
		for r in self.rect_list:
			self.image.fill(DEBUG_TEXT_COLOR, r)
		
		self.rect_list = []
		x = 20
		y = 20
		key_max_length = 10
		text_color = (255, 255, 0)
		
		# update content
		self.content["ticks"] = Engine.game_engine.GameEngine.get_instance().get_running_ticks()
		
		for k in self.content:
			k_str = k.ljust(key_max_length)
			text_surface = self.font.render(k_str + ": " + str(self.content[k]), 0, text_color)
			self.rect_list += [pg.Rect((x, y), text_surface.get_size())]
			self.image.blit(text_surface, (x, y))
			y += int(1.5 * self.font.get_height())
