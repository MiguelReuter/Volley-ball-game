# encoding : UTF-8

from pygame import *
from Engine.Display import Debug3D


class Character:
	def __init__(self, position, w=0.4, h=1.5, max_velocity=4):
		self.position = Vector3(position)
		self.w = w
		self.h = h
		self.max_velocity = max_velocity  # m/s

	def draw(self, display_manager):
		center_pos = Vector3(self.position) + Vector3(0, 0, self.h/2)
		shadow_pos = Vector3(center_pos) - (0, 0, self.h/2)
		Debug3D.draw_horizontal_ellipse(display_manager.camera, shadow_pos, self.w/2)
		Debug3D.draw_aligned_axis_box(display_manager.camera, center_pos, self.w, self.w, self.h)

	def move_rel(self, dxyz):
		self.position += Vector3(dxyz)

	def move(self, b_UP, b_DOWN, b_LEFT, b_RIGHT, dt):
		dxyz = 0.001 * dt * Vector3(b_DOWN - b_UP, b_RIGHT - b_LEFT, 0) * self.max_velocity
		# normalize
		if (b_UP or b_DOWN) and (b_LEFT or b_RIGHT):
			dxyz *= 0.7071  # sqrt(2)
		self.move_rel(dxyz)






