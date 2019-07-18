# encoding : UTF-8

from Engine.Display.camera import Camera
from Settings import *

import pygame as pg

from Engine.Display.sprites_group import HUD, Debug3D, DebugText

SCREEN_COLOR = (0, 0, 50)


class DisplayManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return DisplayManager.s_instance

	def __init__(self):
		self.debug_3d = Debug3D()
		self.debug_text = DebugText()
		self.hud = HUD()
		
		self.screen = None
		self.screen_size = None  # size of screen
		self.scaled_size = None  # size of scaled surface ie f * self.nominal_size
		self.f_scale = 1
		self.rect_list = []
		
		self.camera = Camera(CAMERA_POS, FOCUS_POINT, FOV_ANGLE)
		
		self.create_window()

		DisplayManager.s_instance = self
		
	def create_window(self):
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
		print("scaling window factor:", self.f_scale)
		
		# create pygame window
		if IS_WINDOW_IN_FULL_SCREEN_MODE:
			fl = pg.FULLSCREEN
		else:
			fl = 0
			
		self.screen = pg.display.set_mode(self.screen_size, flags=fl)
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
		# update
		self.debug_3d.update(objects)
		self.debug_text.update()
		self.hud.update()
		
		# update screen
		self.rect_list = self.debug_text.rect_list + self.hud.rect_list + self.debug_3d.rect_list
		# print(self.rect_list)
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
	