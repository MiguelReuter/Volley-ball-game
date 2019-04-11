# encoding : UTF-8

from Engine.Display.camera import Camera
from settings import *

import pygame as pg


class DisplayManager:
	# TODO : singleton
	def __init__(self, game_engine, surface_size=NOMINAL_RESOLUTION, debug_surface_size=None):
		self.game_engine = game_engine
		self.camera = Camera(self, CAMERA_POS, FOCUS_POINT, FOV_ANGLE)
		self.surface = pg.Surface(surface_size)
		self.debug_surface = pg.Surface(debug_surface_size if debug_surface_size is not None else surface_size)
		self.debug_surface.set_colorkey((0, 0, 0))
		
	def update(self, objects):
		self.surface.fill((0, 0, 0))
		self.debug_surface.fill((0, 0, 0))
		for obj in objects:
			obj.draw(self)

	