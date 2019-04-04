# encoding : UTF-8

from Engine.Graphics.camera import Camera
from settings import *


class GraphicsEngine:
	# TODO : singleton
	def __init__(self, game_engine):
		self.game_engine = game_engine
		self.camera = Camera(self, CAMERA_POS, FOCUS_POINT, SCREEN_WIDTH, SCREEN_HEIGHT, FOV_ANGLE)
	