# encoding : UTF-8

from pygame import *
from math import tan, radians, floor
from settings import *


class Camera:
	def __init__(self, graphics_engine, pos, focus_point, w=800, h=640, fov_angle=60):
		self.graphics_engine = graphics_engine
		self.w = w
		self.h = h
		self.position = Vector3(pos)
		self.focus_point = Vector3(focus_point)  # y component will be ignored
		
		self.fov_angle = fov_angle
		self.fov = tan(radians(self.fov_angle))
		
		self.surface = Surface((self.w, self.h))
		
	def world_to_cam_3d_coords(self, w_pt):
		# w vector in world ref
		focus_pt = Vector3(self.focus_point)
		focus_pt.y = self.position.y
		fc = (self.position - focus_pt).normalize()
		
		# translation
		t_pt = w_pt - self.position
		
		# rotation
		sin_a = fc[2]
		cos_a = fc[0]
		
		c_pt = Vector3(t_pt[1],
					   sin_a * t_pt[0] - cos_a * t_pt[2],
					   cos_a * t_pt[0] + sin_a * t_pt[2])
		
		return c_pt
		
	def world_to_pixel_coords(self, pt_3d):
		u, v = 0, 0
		
		pt_3c = self.world_to_cam_3d_coords(pt_3d)
		
		if pt_3c[2] != 0:
			u = int(floor(-self.w / (2 * self.fov) * pt_3c[0] / pt_3c[2]) + self.w / 2)
			v = int(floor(-self.h / (2 * self.fov) * pt_3c[1] / pt_3c[2]) + self.h / 2)
		return u, v