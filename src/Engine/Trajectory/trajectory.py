# encoding : UTF-8target_pos

from pygame import Vector3
from math import sqrt

from Settings import G


class Trajectory:
	def __init__(self, origin_pos=None, target_pos=None, initial_velocity=None):
		self.origin_pos = Vector3(origin_pos) if origin_pos is not None else None
		self.target_pos = Vector3(target_pos) if target_pos is not None else None
		self.initial_velocity = Vector3(initial_velocity) if initial_velocity is not None else None
		self.debug_pts = None
		
		self._set_n_debug_3d_points(n=10)
	
	def _set_n_debug_3d_points(self, n):
		"""
		Process n 3D-points in ball trajectory.

		:param int n: points count
		:return: n points in list
		:rtype list(Vector3):
		"""
		if self.origin_pos is None or self.target_pos is None or self.initial_velocity is None:
			self.debug_pts = []
		else:
			# z_t
			z_t = self.target_pos.z - self.origin_pos.z
			
			# u vector : unit vector in XY plane from origin to target position
			u = Vector3(self.initial_velocity)
			u.z = 0
			u = u.normalize() if u.length_squared() != 0 else Vector3(0, 0, 0)
			
			# find t_t : final time
			a = G / 2
			b = -self.initial_velocity.z
			c = z_t
			
			delta = b ** 2 - 4 * a * c
			assert delta > 0
			t_t = (-b + sqrt(delta)) / (2 * a)
			
			assert n > 1
			dt = t_t / (n - 1)
			self.debug_pts = []
			for i in range(n):
				t_i = i * dt
				u_i = t_i * self.initial_velocity.dot(u)
				z_i = -t_i ** 2 / 2 * G + t_i * self.initial_velocity.z
				self.debug_pts.append(Vector3(u_i * u + self.origin_pos + Vector3(0, 0, z_i)))
	