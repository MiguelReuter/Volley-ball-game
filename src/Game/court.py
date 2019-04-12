# encoding : UTF-8

from Engine.Display import Debug3D

class Court:
	def __init__(self, w, h, net_z1, net_z2):
		self.w = w
		self.h = h
		self.net_z1 = net_z1
		self.net_z2 = net_z2

	def draw(self, display_manager):
		corners_h = 2
		# court ground
		Debug3D.draw_polygon(display_manager,
		                     [(-self.h / 2, -self.w / 2, 0), (-self.h / 2, self.w / 2, 0),
		                      (self.h / 2, self.w / 2, 0), (self.h / 2, -self.w / 2, 0)])

		# corners
		Debug3D.draw_line(display_manager,
		                  (-self.h / 2, -self.w / 2, 0),
		                  (-self.h / 2, -self.w / 2, corners_h))
		Debug3D.draw_line(display_manager,
		                  (-self.h / 2, self.w / 2, 0),
		                  (-self.h / 2, self.w / 2, corners_h))
		Debug3D.draw_line(display_manager,
		                  (self.h / 2, self.w / 2, 0),
		                  (self.h / 2, self.w / 2, corners_h))
		Debug3D.draw_line(display_manager,
		                  (self.h / 2, -self.w / 2, 0),
		                  (self.h / 2, -self.w / 2, corners_h))

		# net
		Debug3D.draw_line(display_manager,
		                  (-self.h / 2, 0, 0),
		                  (-self.h / 2, 0, self.net_z2))
		Debug3D.draw_line(display_manager,
		                  (self.h / 2, 0, 0),
		                  (self.h / 2, 0, self.net_z2))
		Debug3D.draw_line(display_manager,
		                  (-self.h / 2, 0, self.net_z2),
		                  (self.h / 2, 0, self.net_z2))
		Debug3D.draw_line(display_manager,
		                  (-self.h / 2, 0, self.net_z1),
		                  (self.h / 2, 0, self.net_z1))