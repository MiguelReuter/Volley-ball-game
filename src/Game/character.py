# encoding : UTF-8

from pygame import *
from Engine.Display import Debug3D


class Character:
	def __init__(self, position, w=0.4, h=1.5):
		self.position = Vector3(position)
		self.w = w
		self.h = h

	def draw(self, display_manager):
		center_pos = Vector3(self.position) + Vector3(0, 0, self.h/2)
		Debug3D.draw_aligned_axis_box(display_manager.camera, center_pos, self.w, self.w, self.h)

	def move_rel(self, dxyz):
		self.position += Vector3(dxyz)


