# encoding : UTF-8

import pygame as pg
from Engine.Display.scalable_sprite import ScalableSprite
from Settings.general_settings import *

import Engine.game_engine


HUD_COLOR = (100, 100, 0)


class HUD(pg.sprite.LayeredDirty):
	class TimeSprite(ScalableSprite):
		def __init__(self, *groups):
			ScalableSprite.__init__(self, 1.0, *groups)
			self.color = (200, 200, 200)
			self.font = pg.font.Font(FONT_DIR, 8)
			
			self.t = -1
		
		def update(self, *args):
			# update if time changed
			current_t = int(Engine.game_engine.GameEngine.get_instance().get_running_ticks() / 1000)
			if current_t != self.t:
				self.t = current_t
				self.render_text()
			
			f_scale = Engine.Display.display_manager.DisplayManager.get_instance().f_scale
			ScalableSprite.update(self, f_scale)
		
		def render_text(self):
			self.dirty = 1
			
			# update raw image
			t_str = "{}:{:02}".format(int(self.t) // 60, self.t % 60)
			self.set_raw_image(self.font.render(t_str, 0, self.color))
			
			# update raw rect
			t_pos = ((NOMINAL_RESOLUTION[0] - self.raw_image.get_size()[0]) / 2, 10)
			self.prev_rect = self.rect
			self.set_raw_rect(pg.Rect(t_pos, self.raw_image.get_size()))
	
	class ScoreSprite(ScalableSprite):
		def __init__(self, *groups, on_left=True):
			ScalableSprite.__init__(self, 1.0, *groups)
			self.color = (200, 200, 200)
			self.font = pg.font.Font(FONT_DIR, 8)
			self.center_space = 100
			
			self.on_left = on_left
			
			self._score = 0
			self.render_text()
		
		@property
		def score(self):
			return self._score
		
		@score.setter
		def score(self, value):
			self._score = value
			self.render_text()
		
		def render_text(self):
			self.dirty = 1
			
			# update raw image
			self.raw_image = self.font.render(str(self._score), 0, self.color)
			if self.on_left:
				sc_pos = (NOMINAL_RESOLUTION[0] / 2 - self.raw_image.get_size()[0] - self.center_space, 10)
			else:
				sc_pos = (NOMINAL_RESOLUTION[0] / 2 + self.raw_image.get_size()[0] + self.center_space, 10)
			
			# update raw rect
			self.prev_rect = self.rect
			self.set_raw_rect(pg.Rect(sc_pos, self.raw_image.get_size()))
		
		def update(self, *args):
			# rescale if needed to
			f_scale = Engine.Display.display_manager.DisplayManager.get_instance().f_scale
			ScalableSprite.update(self, f_scale)
	
	def __init__(self):
		pg.sprite.LayeredDirty.__init__(self)
		self.font = pg.font.Font(FONT_DIR, 8)
		self.image = None
		self.color = (200, 200, 200)  # TODO: to refactor
		self.time_sprite = None
		self.lscore_sprite = None
		self.rscore_sprite = None
		
		self.rect_list = []
		
		self.create()
	
	def create(self):
		# sprites
		self.time_sprite = HUD.TimeSprite(self)
		self.lscore_sprite = HUD.ScoreSprite(self, on_left=True)
		self.rscore_sprite = HUD.ScoreSprite(self, on_left=False)
		
		self.add(self.time_sprite, self.lscore_sprite, self.rscore_sprite)
		
		# image
		self.create_image(NOMINAL_RESOLUTION)
	
	def create_image(self, size=(0, 0)):
		self.image = pg.Surface(size)
		self.image.fill(HUD_COLOR)
		self.image.set_colorkey(HUD_COLOR)
	
	def update(self):
		pg.sprite.LayeredDirty.update(self)
		
		for sp in self.sprites():
			if sp.dirty > 0:
				self.image.fill(HUD_COLOR, sp.prev_rect)
				self.image.fill(HUD_COLOR, sp.rect)
		
		self.rect_list = pg.sprite.LayeredDirty.draw(self, self.image)
