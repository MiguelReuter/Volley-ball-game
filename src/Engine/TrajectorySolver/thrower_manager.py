# encoding : UTF-8

from pygame import *
from Engine.Display.Debug3D import *
from Engine.TrajectorySolver import *
from Settings import *

import random
from datetime import datetime
random.seed(datetime.now())  # for random throwing


class ThrowerManager:
	"""
	Class used to manage ball throwing.
	"""
	s_instance = None

	@staticmethod
	def get_instance():
		return ThrowerManager.s_instance

	def __init__(self):
		self.target_position = Vector3()
		self.origin_position = Vector3()
		self.debug_trajectory_pts = []

		ThrowerManager.s_instance = self
		
	@staticmethod
	def get_effective_target_position(direction, character_position):
		"""
		Process and get an effective target position for ball throwing depending on character position and direction.
		
		:param pygame.Vector3 direction: direction of throwing
		:param pygame.Vector3 character_position: position of character on the court
		:return: effective target position
		:rtype pygame.Vector3:
		"""
		# TODO : take in account character position
		
		# target pos = court center +/- player direction +/- player position
		# direction
		center = Vector3(THROW_CENTER)
		if character_position.y > 0:
			center.y *= -1
			
		amplified_direction = Vector3(direction)  # [-1, 1]
		for i in (0, 1):
			amplified_direction[i] *= THROW_AMP_DIR[i]
		
		return center + amplified_direction
	
	@staticmethod
	def get_effective_smash_target_position(direction, character_position):
		"""
		Affect target ball position during smash with character's direction and position.
		
		:param pygame.Vector3 direction: direction of smashing
		:param pygame.Vector3 character_position: position of character on the court
		:return: effective target position
		:rtype pygame.Vector3:
		"""
		# TODO : use x direction to orient smash ?
		# TODO : use character attribute "is_in_left_side" for instance
		# center
		center = Vector3(SMASH_CENTER)
		center.x = character_position.x
		if character_position.y > 0:
			center.y *= -1
		
		# control
		amplified_direction = Vector3(direction)  # [-1, 1]
		for i in (0, 1):
			amplified_direction[i] *= SMASH_AMP_DIR[i]
		
		return center + amplified_direction
	
	@staticmethod
	def get_effective_serve_target_position(direction, character_position):
		"""
		Process and get an effective target position for ball serving depending on character position and direction.

		:param pygame.Vector3 direction: direction of throwing
		:param pygame.Vector3 character_position: position of character on the court
		:return: effective target position
		:rtype pygame.Vector3:
		"""
		# direction
		center = Vector3(SERVE_CENTER)
		if character_position.y > 0:
			center.y *= -1
		
		amplified_direction = Vector3(direction)  # [-1, 1]
		for i in (0, 1):
			amplified_direction[i] *= SERVE_AMP_DIR[i]
		
		return center + amplified_direction
	
	def draw(self):
		"""
		Draw debug 3D objects (ball trajectory, target ball position).
		
		:return: None
		"""
		
		# draw target position
		ground_pos = Vector3(self.target_position)
		ground_pos.z = 0
		draw_sphere(self.target_position, 0.1, col=(255, 255, 0))
		draw_line(self.target_position, ground_pos)
		
		# draw trajectory
		for i in range(len(self.debug_trajectory_pts) - 1):
			draw_line(self.debug_trajectory_pts[i], self.debug_trajectory_pts[i + 1], col=(255, 0, 255))

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
			
			# simple throw
			if ev.throwing_type == ThrowingType.THROW and not ball.will_be_served:
				velocity_efficiency = ev.velocity_efficiency
				target_position = self.get_effective_target_position(direction, char_position)
				self.throw_ball(ball, ball.position, target_position, velocity_efficiency=velocity_efficiency)
			# smash (during a jump)
			elif ev.throwing_type == ThrowingType.SMASH and not ball.will_be_served:
				target_position = self.get_effective_smash_target_position(direction, char_position)
				self.smash_ball(ball, ball.position, target_position)
			# serve
			elif ev.throwing_type == ThrowingType.SERVE:
				ball.will_be_served = False
				target_position = self.get_effective_serve_target_position(direction, char_position)
				self.throw_ball(ball, ball.position, target_position, velocity_efficiency=1.0)
			# draft (after diving)
			elif ev.throwing_type == ThrowingType.DRAFT:
				velocity_efficiency = ev.velocity_efficiency
				# TODO : fix ball throwing when origin pos == target pos <-- Vector3(0, 0.01, 0)
				target_position = Vector3(ball.position) + 1 * direction + Vector3(0, 0.01, 0)
				target_position.z = BALL_RADIUS
				self.throw_ball(ball, ball.position, target_position, velocity_efficiency=velocity_efficiency,
								wanted_height=DRAFT_THROW_HEIGHT)

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
		
		event.clear(TRAJECTORY_CHANGED_EVENT)
		
	def smash_ball(self, ball, initial_pos, target_pos):
		"""
		Smash ball from an initial position in the direction of target position.
		
		:param Ball ball: ball to smash
		:param pygame.Vector3 initial_pos: initial position, usually the ball position
		:param pygame.Vector3 target_pos: target position, used to define smash direction
		:return: None
		"""
		velocity = SMASH_VELOCITY * (target_pos - ball.position).normalize()
		
		# process trajectory points for debug display
		self.debug_trajectory_pts = get_n_points_in_trajectory(10, initial_pos, velocity, target_pos.z)
		
		# process target position
		real_target_position = find_target_position(initial_pos, velocity, ball.radius)
		self.target_position = Vector3(real_target_position)
		self.origin_position = Vector3(initial_pos)
		
		# throw the ball
		ball.position = Vector3(initial_pos)
		ball.velocity = Vector3(velocity)
		