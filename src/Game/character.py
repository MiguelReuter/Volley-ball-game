# encoding : UTF-8

from Engine.Display import debug3D_utils
from Engine.Collisions import AABBCollider
from Settings import *
import pygame as pg
from math import sqrt

from Engine.Actions import ActionObject
from Game.character_states import *


class Character(ActionObject):
	def __init__(self, position=None, player_id=PlayerId.PLAYER_ID_1, max_velocity=None, jump_velocity=None):
		ActionObject.__init__(self, player_id)
		self._position = Vector3(position) if position is not None else Vector3()
		self.previous_position = Vector3(self._position)
		self.w = CHARACTER_W
		self.h = CHARACTER_H
		self.collider_relative_position = Vector3()
		self.collider = None
		self.is_colliding_ball = False
		self.max_velocity = max_velocity if max_velocity is not None else RUN_SPEED  # m/s
		self.jump_velocity = jump_velocity if jump_velocity is not None else JUMP_VELOCITY  # m/s
		self.velocity = Vector3()
		self.direction = Vector3()
		
		self.team = Team()
		
		self.state = Idling(self)

		self.set_default_collider()
		
		# sprite
		self.rect = pg.Rect(0, 0, 0, 0)
		self.rect_shadow = pg.Rect(0, 0, 0, 0)

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, value):
		self._position = value
		self.collider.center = self._position + self.collider_relative_position

	def draw_debug(self):
		prev_rect = self.rect
		prev_shadow_rect = self.rect_shadow
		
		ground_pos = Vector3(self.position)
		ground_pos.z = 0
		self.rect_shadow = debug3D_utils.draw_horizontal_ellipse(ground_pos, self.w / 2)
		self.rect = self.collider.draw_debug()
		
		return [prev_shadow_rect.union(self.rect_shadow), prev_rect.union(self.rect)]

	def move_rel(self, dxyz, free_displacement=FREE_DISPLACEMENT):
		"""
		Move object with a certain displacement.

		:param pygame.Vector3 dxyz: displacement
		:param bool free_displacement: True if displacement will be not limited on court
		:return: None
		"""
		self.position += Vector3(dxyz)
		if not free_displacement:
			self.limit_displacement_on_court()
	
	def move(self, direction, dt, free_displacement=FREE_DISPLACEMENT):
		"""
		Move object along a specified direction and amount of time.

		The amplitude of displacement is dependant from :
			- :var direction: magnitude
			- :var self.max_velocity:
			- :var dt:

		:param pygame.Vector3 direction: direction of displacement
		:param float dt: amount of time in ms. Usually, dt is the time between 2 frames
		:param bool free_displacement: True if displacement will be not limited on court
		:return: None
		"""
		dxyz = 0.001 * dt * direction * self.max_velocity
		self.move_rel(dxyz, free_displacement)
	
	def limit_displacement_on_court(self):
		"""
		Limit displacement on court. Called by move_rel method.

		:return: None
		"""
		new_pos = self.position
		
		# net
		if self.team.id == TeamId.LEFT:
			if self.collider.get_bound_coords(axis=1, m_to_p=True) + self.collider_relative_position.y > 0:
				new_pos.y = -self.collider.size3.y / 2 - self.collider_relative_position.y
		else:
			if self.collider.get_bound_coords(axis=1, m_to_p=False) + self.collider_relative_position.y < 0:
				new_pos.y = self.collider.size3.y / 2 - self.collider_relative_position.y

		# out of court
		f = 1.5
		game_engine = Engine.game_engine.GameEngine.get_instance()
		court = game_engine.court
		if self.team.id == TeamId.LEFT:
			new_pos.y = max(-f * court.w / 2, new_pos.y)
		else:
			new_pos.y = min(f * court.w / 2, new_pos.y)
		
		new_pos.x = max(-f * court.h / 2, new_pos.x)
		new_pos.x = min(f * court.h / 2, new_pos.x)
		
		self.position = new_pos
		
	def update_actions(self, action_events, **kwargs):
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		filtered_action_events = self.filter_action_events_by_player_id(action_events)
		
		# state machine :
		# run current state
		self.state.run(filtered_action_events, dt=dt)

		# eventually switch state
		self.state = self.state.next(filtered_action_events, dt=dt)
	
	def update_physics(self, dt, free_displacement=FREE_DISPLACEMENT):
		self.previous_position = Vector3(self.position)
		
		self.velocity += Vector3(0, 0, -0.001 * dt * G)
		self.move_rel(0.001 * dt * self.velocity, free_displacement)
		
	def get_hands_position(self):
		"""
		Return hands position of character in world coordinates.

		:return: hands position
		:rtype pygame.Vector3:
		"""
		dh = Vector3(0, 0, self.h)
		dh.y = self.w / 2
		if not self.team.id == TeamId.LEFT:
			dh.y *= -1
		return self.position + dh

	def set_default_collider(self):
		"""
		Set default AABB Collider.

		:return: None
		"""
		self.collider_relative_position = Vector3(0, 0, self.h / 2)
		collider_size3 = Vector3(self.w, self.w, self.h)

		self.collider = AABBCollider(self._position + self.collider_relative_position, collider_size3)

	def set_diving_collider(self, direction):
		"""
		Set AABB Collider during diving.

		:param pygame.Vector3 direction: direction of diving
		:return: None
		"""
		dive_direction = Vector3(direction)

		collider_size3 = Vector3()
		collider_size3.x = max(self.w, self.h * abs(dive_direction.x))
		collider_size3.y = max(self.w, self.h * abs(dive_direction.y))
		collider_size3.z = self.w
		collider_rel_center = Vector3(self.h / 2 * dive_direction.x,
									  self.h / 2 * dive_direction.y,
									  self.w / 2)
		if dive_direction.x < 0:
			collider_rel_center.x += self.w / 2
		elif dive_direction.x > 0:
			collider_rel_center.x -= self.w / 2

		if dive_direction.y < 0:
			collider_rel_center.y += self.w / 2
		elif dive_direction.y > 0:
			collider_rel_center.y -= self.w / 2

		self.collider_relative_position	= collider_rel_center
		self.collider = AABBCollider(self._position + self.collider_relative_position, collider_size3)
		
	def reset(self):
		self.set_default_collider()
		self.velocity = Vector3()

	def is_state_type_of(self, state_type):
		return self.state.__class__.type == state_type

	def get_time_to_run_to(self, target_position, origin_pos=None):
		"""
		Give time that takes character by running from an origin to a target position.

		Time is processed with displacements in 8 possible directions.
		:param pygame.Vector3 target_position: target position
		:param pygame.Vector3 origin_pos: origin position. Current character position is default value.
		:return: given time in sec
		:rtype: float
		"""
		if origin_pos is None:
			origin_pos = self.position

		# absolute delta position
		delta_pos = target_position - origin_pos
		delta_pos = Vector3([abs(delta_pos[i]) for i in (0, 1, 2)])

		# diagonal travel
		dist_on_each_axis = min(delta_pos.x, delta_pos.y)
		diagonal_time = 1.4142 * dist_on_each_axis / self.max_velocity

		# orthogonal travel
		direct_time = (max(delta_pos.x, delta_pos.y) - dist_on_each_axis) / self.max_velocity

		return diagonal_time + direct_time

	def get_time_to_jump_to_height(self, h):
		"""
		Give time that takes the top of character reaches a specific height by jumping.

		Given time is processed in ascending phase.
		:param float h: height at which time is given
		:return: given time is sec or None if there is no solution
		:rtype: float or None
		"""
		# at t=t1, self.position.z(0) + self.h = h
		# -G / 2 * t1**2 + self.jump_velocity * t1 + self.h - h = 0
		a, b, c = -G/2, self.jump_velocity, self.h - h
		delta = b**2 - 4 * a * c

		if delta >= 0:
			return (-b + sqrt(delta)) / (2 * a)  #
		else:
			return None

	def get_max_height_jump(self):
		"""
		Give max height reached by top of character by jumping.

		:return: max height reached
		:rtype: float
		"""
		a, b, c = -G/2, self.jump_velocity, self.h
		delta = b**2 - 4 * a * c
		return -delta / (4 * a)


class Team:
	def __init__(self, team_id=TeamId.NONE, characters_list=None):
		self.characters = characters_list
		self.score = 0
		self.id = team_id
		self.set_team_to_characters()
	
	def reset(self, **kwargs):
		k = kwargs.keys()
		
		self.characters = kwargs["characters"] if "characters" in k else None
		self.set_team_to_characters()
		
		self.score = kwargs["score"] if "score" in k else 0
		self.id = kwargs["score"] if "score" in k else TeamId.NONE
	
	def add_score(self, val=1):
		self.score += val
	
	def set_team_to_characters(self):
		if self.characters is not None:
			for ch in self.characters:
				ch.team = self