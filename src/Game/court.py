# encoding : UTF-8

from Engine.Display import debug3D
from Engine.Collisions import AABBCollider
from pygame import *


class Court:
	def __init__(self, w, h, net_z1, net_z2):
		self.w = w
		self.h = h
		self.net_z1 = net_z1
		self.net_z2 = net_z2
		self.collider = AABBCollider(Vector3(0, 0, (net_z1 + net_z2) / 2),
		                             (h, 0, net_z2 - net_z1))

	def draw(self):
		self.collider.draw()

		corners_h = 2
		# court ground
		debug3D.draw_polygon([(-self.h / 2, -self.w / 2, 0), (-self.h / 2, self.w / 2, 0),
							  (self.h / 2, self.w / 2, 0), (self.h / 2, -self.w / 2, 0)])

		# corners
		debug3D.draw_line(Vector3(-self.h / 2, -self.w / 2, 0), Vector3(-self.h / 2, -self.w / 2, corners_h))
		debug3D.draw_line(Vector3(-self.h / 2, self.w / 2, 0), Vector3(-self.h / 2, self.w / 2, corners_h))
		debug3D.draw_line(Vector3(self.h / 2, self.w / 2, 0), Vector3(self.h / 2, self.w / 2, corners_h))
		debug3D.draw_line(Vector3(self.h / 2, -self.w / 2, 0), Vector3(self.h / 2, -self.w / 2, corners_h))

		# net
		debug3D.draw_line(Vector3(-self.h / 2, 0, 0), Vector3(-self.h / 2, 0, self.net_z2))
		debug3D.draw_line(Vector3(self.h / 2, 0, 0), Vector3(self.h / 2, 0, self.net_z2))
		debug3D.draw_line(Vector3(-self.h / 2, 0, self.net_z2), Vector3(self.h / 2, 0, self.net_z2))
		debug3D.draw_line(Vector3(-self.h / 2, 0, self.net_z1), Vector3(self.h / 2, 0, self.net_z1))