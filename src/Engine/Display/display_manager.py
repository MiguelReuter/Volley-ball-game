# encoding : UTF-8

from Engine.Display.camera import Camera
from Engine.Display.scalable_sprite import ScalableSprite
from Settings import *

import pygame as pg
from math import log2, pow
from datetime import datetime

import Engine.game_engine


SCREEN_COLOR = (50, 50, 0)
HUD_COLOR = (100, 100, 0)
DEBUG_TEXT_COLOR = (200, 200, 0)
DEBUG_3D_COLOR = (0, 200, 0)



class DisplayManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return DisplayManager.s_instance

	def __init__(self):
		# will be set in self.create_window()
		self.screen = None
		self.unscaled_surface = None
		self.scaled_surface = None
		self.debug_surface = None
		
		self.debug_3d = DisplayManager.Debug3D()
		self.debug_text = DisplayManager.DebugText()
		self.hud = DisplayManager.HUD()

		self.window_mode = WINDOW_MODE
		self.window_resize_2n = WINDOW_RESIZE_2N
		self.screen_scale_factor_2n = None
		self.create_window()
		# self._create_window(NOMINAL_RESOLUTION, self.window_mode, self.window_resize_2n)
		
		# test
		self.screen_size = None  # size of screen
		self.scaled_size = None  # size of scaled surface ie f * self.nominal_size
		self.nominal_size = NOMINAL_RESOLUTION
		self.f_scale = 1
		self.rect_list = []
		
		self._frames_nb = 0
		# end test
		
		self.camera = Camera(CAMERA_POS, FOCUS_POINT, FOV_ANGLE)

		DisplayManager.s_instance = self
		
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
	
	class Debug3D(pg.sprite.GroupSingle):
		"""
		Class for 3D shapes displaying on game window.
		"""
		def __init__(self):
			pg.sprite.GroupSingle.__init__(self)
			self.image = None
			self.rect_list = None
			
		def create_image(self, size=(0, 0)):
			self.image = pg.Surface(size)
			self.image.fill(DEBUG_3D_COLOR)
			self.image.set_colorkey(DEBUG_3D_COLOR)
			
		def update(self, objects):
			DisplayManager.get_instance().debug_surface.fill(DEBUG_3D_COLOR)
			
			for obj in objects:
				obj.draw()
				
			self.image = DisplayManager.get_instance().debug_surface
			self.rect_list = [self.image.get_clip()]
		
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
				
				f_scale = DisplayManager.get_instance().f_scale
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
				f_scale = DisplayManager.get_instance().f_scale
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
			self.time_sprite = DisplayManager.HUD.TimeSprite(self)
			self.lscore_sprite = DisplayManager.HUD.ScoreSprite(self, on_left=True)
			self.rscore_sprite = DisplayManager.HUD.ScoreSprite(self, on_left=False)
			
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
			
	def create_window(self):
		size_2n = True
		
		# size of display (not pygame window)
		display_size = (pg.display.Info().current_w, pg.display.Info().current_h)
	
		# setting pygame window size (screen)
		if size_2n:
			self.f_scale = min(*[int(self.get_highest_power_of_2(display_size[i] / NOMINAL_RESOLUTION[i])) for i in (0, 1)])
		else:
			self.f_scale = min(*[int(display_size[i] / NOMINAL_RESOLUTION[i]) for i in (0, 1)])
		self.scaled_size = [self.f_scale * NOMINAL_RESOLUTION[i] for i in (0, 1)]
		self.screen_size = self.scaled_size  # may be different in fullscreen mode
		print("scaling window factor:", self.f_scale)
		
		# create pygame window
		self.screen = pg.display.set_mode(self.screen_size)
		pg.display.set_caption(CAPTION_TITLE)
		self.screen.fill(SCREEN_COLOR)
		self.screen.set_colorkey(SCREEN_COLOR)
		
		# setting other surfaces
		self.create_surfaces()
		
	def update_screen_size(self, scale_factor=1.0):
		if scale_factor != self.f_scale:
			print("change scale factor to ", scale_factor)
			self.f_scale = scale_factor
			self.create_surfaces()
		
	def create_surfaces(self):
		self.scaled_size = [int(self.f_scale * NOMINAL_RESOLUTION[i]) for i in (0, 1)]
		
		self.debug_surface = pg.Surface(self.scaled_size)
		self.debug_surface.fill(DEBUG_3D_COLOR)
		self.debug_surface.set_colorkey(DEBUG_3D_COLOR)
		
		self.debug_3d.create_image(self.scaled_size)
		self.debug_text.create_image(self.scaled_size)
		self.hud.create_image(self.scaled_size)

		self.screen.fill(SCREEN_COLOR)
		# TODO : must redraw all images !
		pg.display.flip()
	
	def update(self, objects):
		"""
		Update and draw objects each frame.
		
		:param list() objects: list of objects to draw. Each object has to have a method : draw(self, display_manager).
		:return: None
		"""
		print("-------")
		
		# test scale
		modu = 14
		scales = (2.0, 1.0, 0.5, 1.0)
		scale_factor = scales[(self._frames_nb // modu) % len(scales)]
		
		# self.update_screen_size(scale_factor)
		if self._frames_nb % modu == 0:
			self.f_scale = scale_factor
			print("scale change to " + str(self.f_scale))
			self.hud.lscore_sprite.score = int(self._frames_nb)
		self._frames_nb += 1

		# TODO : process for each frame f_scale. If changed,
		# end scale
		
		# update
		self.debug_3d.update(objects)
		self.debug_text.update()
		self.hud.update()
		
		# update screen
		self.rect_list = self.debug_text.rect_list + self.hud.rect_list + self.debug_3d.rect_list
		print(self.rect_list)
		for r in self.rect_list:
			self.screen.fill(SCREEN_COLOR, r)
		
		# TODO : add position_on_screen attribute on hud, debug_text etc. instead of
		#  calling get_position_to_blit_centered_surfaces. This attribute would be updated each frame with
		#  get_position_to_blit_centered_surfaces func or similar
		self.blit_on_screen(self.debug_3d.image)
		self.blit_on_screen(self.debug_text.image)
		self.blit_on_screen(self.hud.image)
		
		# update screen
		pg.display.update(self.rect_list)
		pg.display.flip()
	
	def blit_on_screen(self, image, pos=None, centered=True):
		if pos is None:
			pos = (0, 0)
			if centered:
				pos = tuple(int(self.screen.get_size()[i] / 2 - image.get_size()[i] / 2) for i in (0, 1))
				
		self.screen.blit(image, pos)
		
	
	
	
	@staticmethod
	def get_position_to_blit_centered_surfaces(main_surface_size, surface_to_draw_size):
		"""
		Get position to draw a centered surface onto another.
		
		usage examples:
			>>> DisplayManager.get_position_to_blit_centered_surfaces((50, 100), (10, 10))
			(20, 45)
			>>> DisplayManager.get_position_to_blit_centered_surfaces((50, 100), (1000, 1000))
			(0, 0)
			
		:param tuple(int, int) main_surface_size: size of main surface to draw on
		:param tuple(int, int) surface_to_draw_size: size of surface to draw
		:return: left-top corner position of surface to draw on
		:rtype tuple(int, int):
		"""
		if main_surface_size[0] >= surface_to_draw_size[0] and main_surface_size[1] >= surface_to_draw_size[1]:
			return tuple(int(main_surface_size[i] / 2 - surface_to_draw_size[i] / 2) for i in (0, 1))
		return 0, 0
	
	@staticmethod
	def get_highest_power_of_2(n):
		res = 0
		for i in range(int(n), 0, -1):
			# if i is a power of 2
			if (i & (i - 1)) == 0:
				res = i
				break
		return res


if __name__ == "__main__":
	pg.init()
	
	screen = pg.display.set_mode((100, 100))
	
	screen.fill((0, 0, 0))
	
	surf_b = pg.Surface((100, 100))
	surf_b.fill((100, 50, 0))
	
	t0 = pg.time.get_ticks()
	for _ in range(10000):
		screen.fill((0, 0, 0))
		screen.blit(surf_b, (0, 0))
	pg.display.flip()
	t1 = pg.time.get_ticks()
	
	for _ in range(10000):
		screen.fill((0, 0, 0))
		screen.blit(surf_b, (0, 0))
		pg.display.flip()
	t2 = pg.time.get_ticks()
	
	f_scale = 3
	scaled_surf = pg.Surface([f_scale * surf_b.get_size()[i] for i in (0, 1)])
	
	for _ in range(10000):
		scaled_surf = pg.transform.scale(surf_b, scaled_surf.get_size())
		screen.blit(scaled_surf, (0, 0))
	pg.display.flip()
	t3 = pg.time.get_ticks()

	
	print(t1-t0)
	print(t2-t1)
	print(t3-t2)
	