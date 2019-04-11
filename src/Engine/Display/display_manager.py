# encoding : UTF-8

from Engine.Display.camera import Camera
from settings import *

import pygame as pg
from math import log2, pow


class DisplayManager:
	# TODO : singleton
	def __init__(self, game_engine):
		# will be set in self.create_window()
		self.screen = None
		self.unscaled_surface = None
		self.scaled_surface = None

		self.window_mode = WINDOW_MODE
		self.window_resize_2n = WINDOW_RESIZE_2N
		self.screen_scale_factor_2n = None
		self._create_window()
		
		self.game_engine = game_engine
		self.camera = Camera(self, CAMERA_POS, FOCUS_POINT, FOV_ANGLE)
		
		self.debug_surface = pg.Surface(self.screen.get_size())
		self.debug_surface.set_colorkey((0, 0, 0))
	
	def _create_window(self):
		w, h = NOMINAL_RESOLUTION
		
		fl = pg.RESIZABLE if self.window_mode == WindowMode.RESIZABLE else 0
		
		if self.window_mode == WindowMode.FIXED_SIZE or self.window_mode == WindowMode.RESIZABLE:
			if not self.window_resize_2n:
				pass
			else:
				self.screen_scale_factor_2n = self._process_screen_factor_scale()
				w = int(NOMINAL_RESOLUTION[0] * pow(2, self.screen_scale_factor_2n))
				h = int(NOMINAL_RESOLUTION[1] * pow(2, self.screen_scale_factor_2n))
				
		elif self.window_mode == WindowMode.FULL_SCREEN:
			# TODO : to implement
			print(self.window_mode, " mode not implemented")
		
		self.screen = pg.display.set_mode((w, h), flags=fl)
		self.scaled_surface = pg.Surface((w, h))
		self.unscaled_surface = pg.Surface(NOMINAL_RESOLUTION)
		
		pg.display.set_caption(CAPTION_TITLE)
		
	def _resize_surface(self, surface):
		if self.window_mode == WindowMode.FIXED_SIZE and self.window_resize_2n:
			new_size = list(surface.get_size())
			new_surface = pg.Surface(new_size)
			new_surface.blit(surface, (0, 0))
			for _ in range(self.screen_scale_factor_2n):
				new_size = [new_size[i] * 2 for i in (0, 1)]
				new_surface = pg.transform.scale2x(new_surface)
			return new_surface
		if self.window_mode == WindowMode.RESIZABLE:
			new_size = self.scaled_surface.get_size()
			for event in pg.event.get(pg.VIDEORESIZE):
				new_screen_size = event.size
				f_w, f_h = tuple(new_screen_size[i] / surface.get_size()[i] for i in (0, 1))
				f = min(f_w, f_h)
				self.screen = pg.Surface(new_screen_size)
				new_size = tuple(int(f * surface.get_size()[i]) for i in (0, 1))
				self.scaled_surface = pg.Surface(new_size)
				
			self.debug_surface = pg.transform.scale(self.debug_surface, (new_size))
			return pg.transform.smoothscale(surface, new_size)
		
		return surface
	
	def _process_screen_factor_scale(self):
		f_w = int(log2(pg.display.Info().current_w / NOMINAL_RESOLUTION[0]))
		f_h = int(log2(pg.display.Info().current_h / NOMINAL_RESOLUTION[1]))
		return min(f_w, f_h)
	
	def _get_blit_position(self, size_1, size_2):
		if size_1[0] >= size_2[0] and size_1[1] >= size_2[1]:
			return tuple(int(size_1[i] / 2 - size_2[i] / 2) for i in (0, 1))
		return (0, 0)
	
	def update(self, objects):
		print("---")
		self.screen.fill((50, 50, 0))
		self.unscaled_surface.fill((0, 0, 50))
		self.debug_surface.fill((0, 0, 0))
		for obj in objects:
			obj.draw(self)
		
		# resize
		self.scaled_surface = self._resize_surface(self.unscaled_surface)
		
		print("unscaled :", self.unscaled_surface.get_size())
		print("scaled :", self.scaled_surface.get_size())
		print("debug :", self.debug_surface.get_size())
		print("screen :", self.screen.get_size())

		self.screen.blit(self.scaled_surface, self._get_blit_position(self.screen.get_size(), self.scaled_surface.get_size()))
		self.screen.blit(self.debug_surface, self._get_blit_position(self.screen.get_size(), self.debug_surface.get_size()))
		# update screen
		pg.display.flip()
			
	

	