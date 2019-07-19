# encoding : UTF-8

from pygame import Vector3
import pygame as pg

from Engine.Display import debug3D_utils
from Engine.Collisions import AABBCollider


class Court:
	def __init__(self, w, h, net_z1, net_z2):
		self.w = w
		self.h = h
		self.net_z1 = net_z1
		self.net_z2 = net_z2
		self.collider = AABBCollider(Vector3(0, 0, (net_z1 + net_z2) / 2),
		                             (h, 0, net_z2 - net_z1))
		
		# sprite
		self.rects = [pg.Rect(0, 0, 0, 0) for _ in range(10)]

	def draw_debug(self):
		prev_rects = self.rects.copy()
		
		self.rects[0] = self.collider.draw_debug()

		corners_h = 2
		# court ground
		self.rects[1] = debug3D_utils.draw_polygon([(-self.h / 2, -self.w / 2, 0), (-self.h / 2, self.w / 2, 0),
		                                            (self.h / 2, self.w / 2, 0), (self.h / 2, -self.w / 2, 0)])

		# corners
		self.rects[2] = debug3D_utils.draw_line(Vector3(-self.h / 2, -self.w / 2, 0),
		                                        Vector3(-self.h / 2, -self.w / 2, corners_h))
		self.rects[3] = debug3D_utils.draw_line(Vector3(-self.h / 2, self.w / 2, 0),
		                                        Vector3(-self.h / 2, self.w / 2, corners_h))
		self.rects[4] = debug3D_utils.draw_line(Vector3(self.h / 2, self.w / 2, 0),
		                                        Vector3(self.h / 2, self.w / 2, corners_h))
		self.rects[5] = debug3D_utils.draw_line(Vector3(self.h / 2, -self.w / 2, 0),
		                                        Vector3(self.h / 2, -self.w / 2, corners_h))

		# net
		self.rects[6] = debug3D_utils.draw_line(Vector3(-self.h / 2, 0, 0), Vector3(-self.h / 2, 0, self.net_z2))
		self.rects[7] = debug3D_utils.draw_line(Vector3(self.h / 2, 0, 0), Vector3(self.h / 2, 0, self.net_z2))
		self.rects[8] = debug3D_utils.draw_line(Vector3(-self.h / 2, 0, self.net_z2), Vector3(self.h / 2, 0, self.net_z2))
		self.rects[9] = debug3D_utils.draw_line(Vector3(-self.h / 2, 0, self.net_z1), Vector3(self.h / 2, 0, self.net_z1))
		
		return [prev_rects[i].union(self.rects[i]) for i in range(10)]
	