# encoding : UTF-8

from pygame import *
from Engine.Display.Debug3D import *
from Engine.TrajectorySolver import *

import random
from datetime import datetime
random.seed(datetime.now())  # for random throwing


class ThrowerManager:
	def __init__(self):
		self.target_position = Vector3()
		self.origin_position = Vector3()
		self.debug_trajectory_pts = []
		
	def set_target_position(self):
		# target pos = court center +/- player direction +/- player position
		pass
	
	def draw(self, display_manager):
		# draw target position
		ground_pos = Vector3(self.target_position)
		ground_pos.z = 0
		draw_sphere(display_manager, self.target_position, 0.1, col=(255, 255, 0))
		draw_line(display_manager, self.target_position, ground_pos)
		
		# draw trajectory
		for i in range(len(self.debug_trajectory_pts) - 1):
			draw_line(display_manager, self.debug_trajectory_pts[i], self.debug_trajectory_pts[i + 1],
			          col=(255, 0, 255))

	def throw_at_random_target_position(self, ball, initial_pos, wanted_height, corner_1=None, corner_2=None):
		"""
		Throw ball at random target position in a specified area from an initial position.
		
		:param Ball ball: the ball to throw
		:param pygame.Vector3 initial_pos: initial position of ball in world coordinates
		:param wanted_height: wanted height at net place (or at middle trajectory)
		:param tuple(float, float) corner_1: 1st corner of area, min x and min y
		:param tuple(float, float) corner_2: 2nd corner of area, max x and max y
		:return:
		"""
		if corner_1 is None:
			corner_1 = [-1.5, -5]
		if corner_2 is None:
			corner_2 = [1.5, -2]
		cen = [(corner_1[i] + corner_2[i]) / 2 for i in (0, 1)]
		amp = [(corner_1[i] - corner_2[i]) / 2 for i in (0, 1)]
		
		target_pos = Vector3(2 * random.random(), 2 * random.random(), ball.radius) - (1, 1, 0)  # x and y in ]-1, 1[
		target_pos.x = amp[0] * target_pos.x + cen[0]
		target_pos.y = amp[1] * target_pos.y + cen[1]
		
		self.throw_ball(ball, initial_pos, target_pos, wanted_height)
	
	def update(self, throw_events, trajectory_changes_events, ball):
		for ev in trajectory_changes_events:
			self.target_position = ev.target_pos
		
		for ev in throw_events:
			direction = ev.direction
			char_position = ev.position
			velocity_efficiency = ev.velocity_efficiency
			
			self.throw_ball(ball, ball.position, Vector3(0, 3, ball.radius), velocity_efficiency=velocity_efficiency)
		
	def throw_ball(self, ball, initial_pos, target_pos, wanted_height=4, **kwargs):
		"""
		Throw ball from an initial position to a specified target position.
		
		:param Ball ball:
		:param pygame.Vector3 initial_pos:
		:param pygame.Vector3 target_pos:
		:param float wanted_height:
		:return: None
		"""
		velocity_efficiency = kwargs["velocity_efficiency"] if "velocity_efficiency" in kwargs.keys() else 1
		velocity = velocity_efficiency * find_initial_velocity(initial_pos, target_pos, wanted_height)
		
		# target position changed due to velocity_efficiency
		eff_target_pos = find_target_position(initial_pos, ball.velocity, target_pos.z)
		self.target_position = Vector3(eff_target_pos)
		self.origin_position = Vector3(initial_pos)
		
		# process trajectory points for debug display
		self.debug_trajectory_pts = get_n_points_in_trajectory(10, initial_pos, ball.velocity, target_pos.z)
		
		# throw the ball
		ball.position = Vector3(initial_pos)
		ball.velocity = Vector3(velocity)