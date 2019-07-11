# encoding : UTF-8

from Engine.Display.camera import Camera
from Engine.Display.scalable_sprite import ScalableSprite
from Settings import *

import pygame as pg
from math import log2, pow
from datetime import datetime

import Engine.game_engine


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
			self.rect_list = None
			
			self.create()
		
		def create(self):
			self.image = pg.Surface((pg.display.Info().current_w, pg.display.Info().current_h))
			self.image.fill((0, 0, 0))
			self.image.set_colorkey((0, 0, 0))
			self.rect_list = []
		
		def update(self):
			# pg.sprite.GroupSingle.update(self)
			self.create()

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
	
	class HUD(pg.sprite.LayeredDirty):
		class TimeSprite(ScalableSprite):
			def __init__(self, *groups):
				# pg.sprite.DirtySprite.__init__(self, *groups)
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
			self.image = pg.Surface(NOMINAL_RESOLUTION)
			self.scaled_surface = None
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
			self.image.fill((0, 0, 0))
			self.image.set_colorkey((0, 0, 0))
		
		def update(self):
			pg.sprite.LayeredDirty.update(self)

			for sp in self.sprites():
				if sp.dirty > 0:
					self.image.fill((0, 0, 0), sp.prev_rect)
					self.image.fill((0, 0, 0), sp.rect)

			self.rect_list = pg.sprite.LayeredDirty.draw(self, self.image)
			
	def _create_window(self, nominal_resolution, window_mode=WindowMode.FIXED_SIZE, window_resize_2n=False):
		"""
		Create Game Window.
		
		:param tuple(int, int) nominal_resolution: nominal pixel resolution
		:param WindowMode.Enum window_mode: rendered mode of window. Can be FIXED_SIZE, RESIZABLE or FULL_SCREEN
		:param bool window_resize_2n: if True, window size is set to maximum according to your current display
		with a factor 2^n. Nominal resolution is unchanged. Only in FIXED_SIZE and RESIZABLE modes
		:return: None
		"""
		scaled_size = nominal_resolution
		screen_size = nominal_resolution
		fl = 0
		
		if window_mode == WindowMode.FIXED_SIZE or window_mode == WindowMode.RESIZABLE:
			fl = pg.RESIZABLE if window_mode == WindowMode.RESIZABLE else 0
			if not window_resize_2n:
				pass
			else:
				self.screen_scale_factor_2n = self._process_screen_factor_scale()
				scaled_size = tuple(int(nominal_resolution[i] * pow(2, self.screen_scale_factor_2n)) for i in (0, 1))
				screen_size = scaled_size
				
		elif window_mode == WindowMode.FULL_SCREEN:
			fl = pg.FULLSCREEN
			screen_size = pg.display.Info().current_w, pg.display.Info().current_h
			
			f_w, f_h = tuple(screen_size[i] / nominal_resolution[i] for i in (0, 1))
			f = min(f_w, f_h)
			scaled_size = tuple(int(f * nominal_resolution[i]) for i in (0, 1))
		
		self.unscaled_surface = pg.Surface(nominal_resolution)
		self.hud.surface = pg.Surface(nominal_resolution)
		self.hud.scaled_surface = pg.Surface(scaled_size)
		self.scaled_surface = pg.Surface(scaled_size)
		self.debug_surface = pg.Surface(scaled_size)
		self.debug_surface.set_colorkey((0, 0, 0))
		
		self.screen = pg.display.set_mode(screen_size, flags=fl)
		pg.display.set_caption(CAPTION_TITLE)
		self.screen.fill((50, 50, 0))
		pg.display.flip()
		
	def _resize_display(self):
		"""
		Resize display for each frame.
		
		Resize display according to attributes :
			- :var WindowMode.Enum self.window_mode:
			- :var bool self.window_resize_2n values:
		:return: None
		"""
		surface = self.unscaled_surface
		hud_surface = self.hud.image
		
		if self.window_mode == WindowMode.FIXED_SIZE and self.window_resize_2n:
			new_size = list(surface.get_size())
			
			new_surface = pg.Surface(new_size)
			new_surface.blit(surface, (0, 0))
			
			# hud
			new_hud_surface = pg.Surface(new_size)
			new_hud_surface.blit(hud_surface, (0, 0))
			for _ in range(self.screen_scale_factor_2n):
				new_size = [new_size[i] * 2 for i in (0, 1)]
				self.scaled_surface = pg.transform.scale2x(new_surface)
				self.hud.scaled_surface = pg.transform.scale2x(new_hud_surface)
				
		elif self.window_mode == WindowMode.RESIZABLE:
			scaled_size = self.scaled_surface.get_size()
			for event in pg.event.get(pg.VIDEORESIZE):
				new_screen_size = event.size
				self.screen = pg.display.set_mode(new_screen_size, flags=pg.RESIZABLE)
				
				# process size for displayed surfaces
				f_w, f_h = tuple(new_screen_size[i] / self.unscaled_surface.get_size()[i] for i in (0, 1))
				f = min(f_w, f_h)
				scaled_size = tuple(int(f * self.unscaled_surface.get_size()[i]) for i in (0, 1))
				
			# TODO : use smoothscale instead of scale ?
			self.scaled_surface = pg.transform.scale(self.unscaled_surface, scaled_size)
			self.debug_surface = pg.transform.scale(self.debug_surface, scaled_size)
			self.hud.scaled_surface = pg.transform.scale(self.hud.image, scaled_size)
		elif self.window_mode == WindowMode.FULL_SCREEN:
			scaled_size = self.scaled_surface.get_size()
			self.scaled_surface = pg.transform.scale(self.unscaled_surface, scaled_size)
			self.hud.scaled_surface = pg.transform.scale(self.hud.image, scaled_size)
		else:
			self.scaled_surface = self.unscaled_surface.copy()
	
	def create_window(self):
		self.screen = pg.display.set_mode(NOMINAL_RESOLUTION, flags=pg.RESIZABLE)
		pg.display.set_caption(CAPTION_TITLE)
		
		self.recreate_window(1.0)
		
	def update_screen_size(self):
		screen_size = (pg.display.Info().current_w, pg.display.Info().current_h)
		print(screen_size)  # not good
		self.screen = pg.Surface(screen_size)
		
		# process size for displayed surfaces
		f_w, f_h = tuple(self.screen.get_size()[i] / NOMINAL_RESOLUTION[i] for i in (0, 1))
		scale_factor = min(f_w, f_h)
		
		if scale_factor != self.f_scale:
			self.recreate_window(scale_factor)
		
	def recreate_window(self, scale_factor):
		print("change size ", scale_factor)
		self.hud.image = pg.Surface(NOMINAL_RESOLUTION)
		
		self.f_scale = scale_factor
		scaled_size = [int(scale_factor * NOMINAL_RESOLUTION[i]) for i in (0, 1)]
		
		self.debug_surface = pg.Surface(scaled_size)
		self.debug_text.image = pg.Surface(scaled_size)
		
		screen_size = (pg.display.Info().current_w, pg.display.Info().current_h)
		self.screen = pg.Surface(screen_size)

		#self.screen.fill((50, 50, 100))
		
		# TODO : must redraw all images !
		pg.display.flip()
	
	@staticmethod
	def _process_screen_factor_scale():
		"""
		Process a factor (2^n) to adapt window size.
		
		:return: None
		"""
		f_w = int(log2(pg.display.Info().current_w / NOMINAL_RESOLUTION[0]))
		f_h = int(log2(pg.display.Info().current_h / NOMINAL_RESOLUTION[1]))
		return min(f_w, f_h)
	
	def update(self, objects):
		"""
		Update and draw objects each frame.
		
		:param list() objects: list of objects to draw. Each object has to have a method : draw(self, display_manager).
		:return: None
		"""
		print("-------")
		
		# test scale
		"""
		self._frames_nb += 1
		modu = 14
		scales = (0.5, 1.0, 1.5, 1.0)
		scale_factor = scales[(self._frames_nb // modu) % len(scales)]
		#self.recreate_window(scale_factor)
		if self._frames_nb % modu == 0:
			print("scale change to " + str(self.f_scale))
			self.hud.lscore_sprite.score = int(self._frames_nb)
		
		self.scaled_size = (self.f_scale * self.nominal_size[i] for i in (0, 1))
		self.screen_size = self.screen.get_size()
		"""
		self.update_screen_size()
		
		
		# TODO : process for each frame f_scale. If changed,
		# end scale

		self.screen.fill((50, 50, 0))
		# self.screen.set_colorkey((50, 50, 0))
		# self.unscaled_surface.fill((100, 0, 50))
		# self.debug_surface.fill((100, 0, 0))
		
		# update
		self.debug_text.update()
		self.hud.update()
		
		for obj in objects:
			obj.draw()
		
		# self._resize_display()
		
		# TODO : add position_on_screen attribute on hud, debug_text etc. instead of
		#  calling get_position_to_blit_centered_surfaces. This attribute would be updated each frame with
		#  get_position_to_blit_centered_surfaces func or similar
		# self.screen.blit(self.scaled_surface, self.get_position_to_blit_centered_surfaces(self.screen.get_size(), self.scaled_surface.get_size()))
		# self.screen.blit(self.debug_surface, self.get_position_to_blit_centered_surfaces(self.screen.get_size(), self.debug_surface.get_size()))
		#self.screen.blit(self.debug_text.image, self.get_position_to_blit_centered_surfaces(self.screen.get_size(),
		#                                                                                   self.debug_text.image.get_size()))
		self.screen.blit(self.hud.image, self.get_position_to_blit_centered_surfaces(self.screen.get_size(),
		                                                                             self.hud.image.get_size()))
		
		
		# update screen
		rect_list = self.debug_text.rect_list + self.hud.rect_list
		pg.display.update(rect_list)
		# pg.display.flip()
	
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
	