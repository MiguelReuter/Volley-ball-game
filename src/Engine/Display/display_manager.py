# encoding : UTF-8

from Engine.Display.camera import Camera
from Settings import *

import pygame as pg

from Engine.Display.sprites_group import HUD, Debug3D, DebugText, Scene3D


class DisplayManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return DisplayManager.s_instance

	def __init__(self):
		DisplayManager.s_instance = self

		self.camera = Camera(CAMERA_POS, FOCUS_POINT, FOV_ANGLE)

		self.scene_3d = Scene3D()
		self.debug_3d = Debug3D()
		self.debug_text = DebugText()
		self.hud = HUD()

		self.screen = None
		self.screen_size = None  # size of screen
		self.scaled_size = None  # size of scaled surface ie f * self.nominal_size
		self.f_scale = 1
		self.rect_list = []

		self.create_window()

	def create_window(self):
		"""
		Create pygame window and different images.
		
		:return: None
		"""
		# size of display (not pygame window yet)
		display_size = (pg.display.Info().current_w, pg.display.Info().current_h)
		
		if FORCE_WINDOW_SCALE_FACTOR is not None:
			self.f_scale = FORCE_WINDOW_SCALE_FACTOR
		else:
			# if scale factor is a power of 2
			if IS_WINDOW_SCALE_FACTOR_2POW:
				self.f_scale = min(*[self.get_highest_power_of_2(display_size[i] / NOMINAL_RESOLUTION[i]) for i in (0, 1)])
			else:
				self.f_scale = min(*[display_size[i] / NOMINAL_RESOLUTION[i] for i in (0, 1)])
			
			# if scale factor is int or not
			if IS_WINDOW_SCALE_FACTOR_INT:
				self.f_scale = int(self.f_scale)
				
		self.scaled_size = [int(self.f_scale * NOMINAL_RESOLUTION[i]) for i in (0, 1)]
		self.screen_size = self.scaled_size  # may be different in fullscreen mode
		
		# create pygame window
		if IS_WINDOW_IN_FULL_SCREEN_MODE:
			fl = pg.FULLSCREEN
		else:
			fl = 0
			
		self.screen = pg.display.set_mode(self.screen_size, flags=fl)
		pg.display.set_caption(CAPTION_TITLE)
		self.screen.fill(BKGND_SCREEN_COLOR)
		self.screen.set_colorkey(BKGND_SCREEN_COLOR)
		
		# setting other surfaces
		self.create_surfaces()
		
	def create_surfaces(self):
		"""
		Create different images.
		
		:return: None
		"""
		self.scaled_size = [int(self.f_scale * NOMINAL_RESOLUTION[i]) for i in (0, 1)]

		self.scene_3d.create_image(self.scaled_size)
		self.debug_3d.create_image(self.scaled_size)
		self.debug_text.create_image(self.scaled_size)
		self.hud.create_image(self.scaled_size)

		self.screen.fill(BKGND_SCREEN_COLOR)
		pg.display.flip()
	
	def update(self, objects):
		"""
		Update and draw objects each frame.
		
		:param list() objects: list of objects to draw. Each object has to have a draw_debug() method.
		:return: None
		"""
		# update
		self.scene_3d.update()
		self.debug_3d.update(objects)
		self.debug_text.update()
		self.hud.update()
		
		# update screen
		self.rect_list = self.debug_text.rect_list + self.hud.rect_list + self.debug_3d.rect_list + self.scene_3d.rect_list
		for r in self.rect_list:
			self.screen.fill(BKGND_SCREEN_COLOR, r)

		self.blit_on_screen(self.scene_3d.image)
		self.blit_on_screen(self.debug_3d.image)
		self.blit_on_screen(self.debug_text.image)
		self.blit_on_screen(self.hud.image)
		
		# update screen
		pg.display.update(self.rect_list)
	
	def blit_on_screen(self, image, pos=None, centered=True):
		"""
		Blit an image on screen.
		
		:param pygame.Surface image: image to blit on screen
		:param tuple(int, int) pos: pos of blitting.
		:param bool centered: If :param pos: is not specified, pos will be set to (0, 0) if :var centered: is False,
		else, :var pos: will be processed to center :var image: on screen.
		:return:
		"""
		if pos is None:
			pos = (0, 0)
			if centered:
				pos = tuple(int(self.screen.get_size()[i] / 2 - image.get_size()[i] / 2) for i in (0, 1))
				
		self.screen.blit(image, pos)
	
	@staticmethod
	def get_highest_power_of_2(n):
		"""
		Get highest power of 2 lower than given value.
		
		:param float n: value
		:return: power of 2
		:rtype int
		"""
		res = 0
		for i in range(int(n), 0, -1):
			# if i is a power of 2
			if (i & (i - 1)) == 0:
				res = i
				break
		return res
	