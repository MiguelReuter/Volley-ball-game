# encoding : UTF-8

import pygame as pg

import Engine.game_engine
from Engine.Display.scalable_sprite import ScalableSprite
from Settings.general_settings import *


class HUD(pg.sprite.LayeredDirty):
	"""
	Dirty Sprites Layer Class for HUD.
	"""
	class TimeSprite(ScalableSprite):
		"""
		Sprite class for Timer.
		"""
		def __init__(self, *groups):
			ScalableSprite.__init__(self, 1.0, *groups)
			self.color = HUD_FONT_COLOR
			self.font = pg.font.Font(FONT_DIR, 8)
			
			self.t = -1
		
		def update(self, *args):
			"""
			Update by checking if ticks changed.
			
			This method is an override of Sprite.update(*args).
			:param args:
			:return: None
			"""
			# update if time changed
			current_t = int(Engine.game_engine.GameEngine.get_instance().get_running_ticks() / 1000)
			if current_t != self.t:
				self.t = current_t
				self.render_text()
			
			f_scale = Engine.Display.display_manager.DisplayManager.get_instance().f_scale
			ScalableSprite.update(self, f_scale)
		
		def render_text(self):
			"""
			Force text rendering and update :var image: and :var rect: attributes.
			
			:return: None
			"""
			self.dirty = 1
			
			# update raw image
			t_str = "{}:{:02}".format(int(self.t) // 60, self.t % 60)
			self.set_raw_image(self.font.render(t_str, 0, self.color))

			# update raw rect
			t_pos = ((NOMINAL_RESOLUTION[0] - self.raw_image.get_size()[0]) / 2, 10)
			self.set_raw_rect(pg.Rect(t_pos, self.raw_image.get_size()))
	
	class ScoreSprite(ScalableSprite):
		"""
		Sprite class for a score.
		"""
		def __init__(self, *groups, on_left=True):
			ScalableSprite.__init__(self, 1.0, *groups)
			self.color = HUD_FONT_COLOR
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
			"""
			Force text rendering and update :var image: and :var rect: attributes.

			:return: None
			"""
			self.dirty = 1
			
			# update raw image
			self.set_raw_image(self.font.render(str(self._score), 0, self.color))
			if self.on_left:
				sc_pos = (NOMINAL_RESOLUTION[0] / 2 - self.raw_image.get_size()[0] - self.center_space, 10)
			else:
				sc_pos = (NOMINAL_RESOLUTION[0] / 2 - self.raw_image.get_size()[0] + self.center_space, 10)
			
			# update raw rect
			self.set_raw_rect(pg.Rect(sc_pos, self.raw_image.get_size()))
		
		def update(self, *args):
			"""
			Update if scale factor changed.

			This method is an override of Sprite.update(*args).
			:param args:
			:return: None
			"""
			# update score
			game_engine = Engine.game_engine.GameEngine.get_instance()
			team_id = TeamId.LEFT if self.on_left else TeamId.RIGHT
			team = game_engine.teams[team_id]
			if team.score != self.score:
				self.score = team.score
			
			# rescale if needed to
			f_scale = Engine.Display.display_manager.DisplayManager.get_instance().f_scale
			ScalableSprite.update(self, f_scale)

	def __init__(self):
		pg.sprite.LayeredDirty.__init__(self)
		self.font = pg.font.Font(FONT_DIR, 8)
		self.image = None
		
		self.time_sprite = None
		self.lscore_sprite = None
		self.rscore_sprite = None
		
		self.rect_list = []
		
		self.create()
	
	def create(self):
		"""
		Create sprites and :var image: attribute.
		
		:return: None
		"""
		# sprites
		self.time_sprite = HUD.TimeSprite(self)
		self.lscore_sprite = HUD.ScoreSprite(self, on_left=True)
		self.rscore_sprite = HUD.ScoreSprite(self, on_left=False)
		
		self.add(self.time_sprite, self.lscore_sprite, self.rscore_sprite)
		
		# image
		self.create_image(NOMINAL_RESOLUTION)
	
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

		For each frame, sprites that need to be redraw are cleared and draw.

		:return: None
		"""
		pg.sprite.LayeredDirty.update(self)
		
		for sp in self.sprites():
			if sp.dirty > 0:
				for r in sp.rect_list_to_redraw + sp.rect_list_to_erase:
					self.image.fill(BKGND_TRANSPARENCY_COLOR, r)
		
		self.rect_list = pg.sprite.LayeredDirty.draw(self, self.image)
