# encoding : UTF-8target_pos

from pygame import Vector3

from Engine import game_engine
from Engine.Trajectory.trajectory_solver import get_time_at_z
from Settings import G


class Trajectory:
	def __init__(self, origin_pos=None, target_pos=None, initial_velocity=None):
		self.origin_pos = Vector3(origin_pos) if origin_pos is not None else None
		self.target_pos = Vector3(target_pos) if target_pos is not None else None
		self.initial_velocity = Vector3(initial_velocity) if initial_velocity is not None else None

		self.t0 = None
		self.debug_pts = None

		self._create()

	def _create(self):
		g_e = game_engine.GameEngine.get_instance()
		self.t0 = g_e.get_running_ticks() if g_e is not None else 0
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
			assert n > 1

			# u vector : unit vector in XY plane from origin to target position
			u = Vector3(self.initial_velocity)
			u.z = 0
			u = u.normalize() if u.length_squared() != 0 else Vector3(0, 0, 0)
			
			# get t_t : final time
			t_t = self.get_final_time()
			
			dt = t_t / (n - 1)
			self.debug_pts = []
			for i in range(n):
				t_i = i * dt
				u_i = t_i * self.initial_velocity.dot(u)
				z_i = -t_i ** 2 / 2 * G + t_i * self.initial_velocity.z
				self.debug_pts.append(Vector3(u_i * u + self.origin_pos + Vector3(0, 0, z_i)))

	def get_final_time(self):
		"""
		Get final time for trajectory.

		:return: time in sec
		:rtype float:
		"""
		return get_time_at_z(self.initial_velocity.z, self.origin_pos.z, self.target_pos.z)

	def get_time_at_z(self, z):
		"""
		Get time at specific height for trajectory descending phase.

		:param float z: target z value
		:return: time in sec which when z is reached
		:rtype float:
		"""
		return get_time_at_z(self.initial_velocity.z, self.origin_pos.z, z)
