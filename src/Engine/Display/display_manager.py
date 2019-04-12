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
		self.debug_surface = None

		self.window_mode = WINDOW_MODE
		self.window_resize_2n = WINDOW_RESIZE_2N
		self.screen_scale_factor_2n = None
		self._create_window()
		
		self.game_engine = game_engine
		self.camera = Camera(self, CAMERA_POS, FOCUS_POINT, FOV_ANGLE)

	def _create_window(self):
		scaled_size = NOMINAL_RESOLUTION
		screen_size = NOMINAL_RESOLUTION
		fl = 0
		
		if self.window_mode == WindowMode.FIXED_SIZE or self.window_mode == WindowMode.RESIZABLE:
			fl = pg.RESIZABLE if self.window_mode == WindowMode.RESIZABLE else 0
			if not self.window_resize_2n:
				pass
			else:
				self.screen_scale_factor_2n = self._process_screen_factor_scale()
				scaled_size = tuple(int(NOMINAL_RESOLUTION[i] * pow(2, self.screen_scale_factor_2n)) for i in (0, 1))
				screen_size = scaled_size
				
		elif self.window_mode == WindowMode.FULL_SCREEN:
			fl = pg.FULLSCREEN
			screen_size = pg.display.Info().current_w, pg.display.Info().current_h
			print(screen_size)
			
			f_w, f_h = tuple(screen_size[i] / NOMINAL_RESOLUTION[i] for i in (0, 1))
			f = min(f_w, f_h)
			scaled_size = tuple(int(f * NOMINAL_RESOLUTION[i]) for i in (0, 1))
		
		self.unscaled_surface = pg.Surface(NOMINAL_RESOLUTION)
		self.scaled_surface = pg.Surface(scaled_size)
		self.debug_surface = pg.Surface(scaled_size)
		self.debug_surface.set_colorkey((0, 0, 0))
		
		self.screen = pg.display.set_mode(screen_size, flags=fl)
		pg.display.set_caption(CAPTION_TITLE)
		
	def resize_display(self):
		surface = self.unscaled_surface
		if self.window_mode == WindowMode.FIXED_SIZE and self.window_resize_2n:
			new_size = list(surface.get_size())
			new_surface = pg.Surface(new_size)
			new_surface.blit(surface, (0, 0))
			for _ in range(self.screen_scale_factor_2n):
				new_size = [new_size[i] * 2 for i in (0, 1)]
				self.scaled_surface = pg.transform.scale2x(new_surface)
				
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
		elif self.window_mode == WindowMode.FULL_SCREEN:
			scaled_size = self.scaled_surface.get_size()
			self.scaled_surface = pg.transform.scale(self.unscaled_surface, scaled_size)
		else:
			self.scaled_surface = self.unscaled_surface.copy()
	
	def _process_screen_factor_scale(self):
		f_w = int(log2(pg.display.Info().current_w / NOMINAL_RESOLUTION[0]))
		f_h = int(log2(pg.display.Info().current_h / NOMINAL_RESOLUTION[1]))
		return min(f_w, f_h)
	
	@staticmethod
	def _get_position_to_blit_centered_surfaces(size_1, size_2):
		"""
		Get position to draw a centered surface onto another.
		
		:param tuple(int, int) size_1: size of surface to draw on
		:param tuple(int, int) size_2: size of surface to draw
		:return: left-top corner position of surface to draw on
		:rtype tuple(int, int):
		"""
		if size_1[0] >= size_2[0] and size_1[1] >= size_2[1]:
			return tuple(int(size_1[i] / 2 - size_2[i] / 2) for i in (0, 1))
		return (0, 0)
	
	def update(self, objects):
		self.screen.fill((50, 50, 0))
		self.unscaled_surface.fill((0, 0, 50))
		self.debug_surface.fill((0, 0, 0))
		for obj in objects:
			obj.draw(self)
		
		self.resize_display()
		
		self.screen.blit(self.scaled_surface, self._get_position_to_blit_centered_surfaces(self.screen.get_size(), self.scaled_surface.get_size()))
		self.screen.blit(self.debug_surface, self._get_position_to_blit_centered_surfaces(self.screen.get_size(), self.debug_surface.get_size()))
		# update screen
		pg.display.flip()
			
	

	