# encoding : UTF-8

from Engine.Display.camera import Camera
from settings import *


class DisplayManager:
	# TODO : singleton
	def __init__(self, game_engine):
		self.game_engine = game_engine
		self.camera = Camera(self, CAMERA_POS, FOCUS_POINT, *NOMINAL_RESOLUTION, FOV_ANGLE)

	def update(self, objects):
		self.camera.surface.fill((0, 0, 0))
		for obj in objects:
			obj.draw(self)

	