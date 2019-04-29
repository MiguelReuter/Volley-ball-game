# encoding : UTF-8

from pygame import *
from Engine.Display.Debug3D import *
from Engine.TrajectorySolver import *
from Settings import SMASH_VELOCITY

import random
from datetime import datetime
random.seed(datetime.now())  # for random throwing


class ThrowerManager:
	def __init__(self):
		self.target_position = Vector3()
		self.origin_position = Vector3()
		self.debug_trajectory_pts = []
		
	@staticmethod
	def get_effective_target_position(direction, character_position, target_z=0):
		"""
		Process and get an effective target position for ball throwing depending on character position and direction.
		
		:param pygame.Vector3 direction: direction of throwing
		:param pygame.Vector3 character_position: position of character on the court
		:param float target_z: height wanted for target position, usually ball radius
		:return: effective target position
		:rtype pygame.Vector3:
		"""
		# TODO : take in account character position and refactor AMP
		AMP = (2, 1.4)
		
		# target pos = court center +/- player direction +/- player position
		# direction
		center = Vector3(0, 3, target_z)
		if character_position.y > 0:
			center.y *= -1
			
		amplified_direction = Vector3(direction)  # [-1, 1]
		amplified_direction.x *= AMP[0]
		amplified_direction.y *= AMP[1]
		
		return center + amplified_direction
	
	@staticmethod
	def get_effective_smash_target_position(direction, character_position, target_z=0):
		"""
		Affect target ball position during smash with character's direction and position.
		
		:param pygame.Vector3 direction: direction of smashing
		:param pygame.Vector3 character_position: position of character on the court
		:param float target_z: height wanted for target position, usually ball radius
		:return: effective target position
		:rtype pygame.Vector3:
		"""
		# TODO : refactor AMP
		# TODO : use x direction to orient smash ?
		AMP = 1.4
		
		# TODO : use character attribute "is_in_left_side" for instance
		center = Vector3(0, 4, target_z)
		if character_position.y > 0:
			center.y *= -1
			
		return Vector3(character_position.x, center.y + direction.y * AMP, target_z)
	
	
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
			if ev.is_smashed:
				target_position = self.get_effective_smash_target_position(direction, char_position,
				                                                           target_z=ball.radius)
				self.smash_ball(ball, ball.position, target_position)
				
			else:
				velocity_efficiency = ev.velocity_efficiency
				target_position = self.get_effective_target_position(direction, char_position, target_z=ball.radius)
				self.throw_ball(ball, ball.position, target_position, velocity_efficiency=velocity_efficiency)
		
	def throw_ball(self, ball, initial_pos, target_pos, wanted_height=4, **kwargs):
		"""
		Throw ball from an initial position to a specified target position.
		
		:param Ball ball: ball to throw
		:param pygame.Vector3 initial_pos: initial position, usually the ball position
		:param pygame.Vector3 target_pos: target position
		:param float wanted_height: desired height at net place
		:return: None
		"""
		velocity_efficiency = kwargs["velocity_efficiency"] if "velocity_efficiency" in kwargs.keys() else 1
		velocity = velocity_efficiency * find_initial_velocity(initial_pos, target_pos, wanted_height)
		
		# target position changed due to velocity_efficiency
		eff_target_pos = find_target_position(initial_pos, velocity, target_pos.z)
		self.target_position = Vector3(eff_target_pos)
		self.origin_position = Vector3(initial_pos)
		
		# process trajectory points for debug display
		self.debug_trajectory_pts = get_n_points_in_trajectory(10, initial_pos, velocity, target_pos.z)
		
		# throw the ball
		ball.position = Vector3(initial_pos)
		ball.velocity = Vector3(velocity)
		
	def smash_ball(self, ball, initial_pos, target_pos):
		"""
		Smash ball from an initial position in the direction of target position.
		
		:param Ball ball: ball to smash
		:param pygame.Vector3 initial_pos: initial position, usually the ball position
		:param pygame.Vector3 target_pos: target position, used to define smash direction
		:return: None
		"""
		velocity = SMASH_VELOCITY * (target_pos - ball.position).normalize()
		
		self.target_position = Vector3(target_pos)
		self.origin_position = Vector3(initial_pos)
		
		# process trajectory points for debug display
		self.debug_trajectory_pts = get_n_points_in_trajectory(10, initial_pos, velocity, target_pos.z)
		
		# throw the ball
		ball.position = Vector3(initial_pos)
		ball.velocity = Vector3(velocity)
		