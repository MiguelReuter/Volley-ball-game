# encoding : UTF-8

from Engine.Display import debug3D_utils
from Engine.Collisions import AABBCollider
from Settings import *
import pygame as pg


from Engine.Actions import ActionObject
from Game.character_states import *


class Character(ActionObject):
	def __init__(self, position, player_id=PlayerId.PLAYER_ID_1, max_velocity=4, is_in_left_side=True):
		ActionObject.__init__(self, player_id)
		self._position = Vector3(position)
		self.previous_position = Vector3()
		self.w = CHARACTER_W
		self.h = CHARACTER_H
		self.collider_relative_position = Vector3()
		self.collider = None
		self.is_colliding_ball = False
		self.max_velocity = max_velocity  # m/s
		self.velocity = Vector3()
		self.direction = Vector3()
		
		self.is_in_left_side = is_in_left_side
		self.team = Team.LEFT if is_in_left_side else Team.RIGHT
		
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

	def move_rel(self, dxyz):
		"""
		Move object with a certain displacement.

		:param pygame.Vector3 dxyz: displacement
		:return: None
		"""
		self.position += Vector3(dxyz)

	def move(self, direction, dt):
		"""
		Move object along a specified direction and amount of time.

		The amplitude of displacement is dependant from :
			- :var direction: magnitude
			- :var self.max_velocity:
			- :var dt:

		:param pygame.Vector3 direction: direction of displacement.
		:param float dt: amount of time in ms. Usually, dt is the time between 2 frames.
		:return: None
		"""
		dxyz = 0.001 * dt * direction * self.max_velocity
		self.move_rel(dxyz)
		
	def update_actions(self, action_events, **kwargs):
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		filtered_action_events = self.filter_action_events_by_player_id(action_events)
		
		# state machine :
		# run current state
		self.state.run(filtered_action_events, dt=dt)

		# eventually switch state
		self.state = self.state.next(filtered_action_events, dt=dt)
	
	def update_physics(self, dt):
		self.previous_position = Vector3(self.position)
		
		self.velocity += Vector3(0, 0, -0.001 * dt * G)
		self.move_rel(0.001 * dt * self.velocity)
		
	def get_hands_position(self):
		"""
		Return hands position of character in world coordinates.

		:return: hands position
		:rtype pygame.Vector3:
		"""
		dh = Vector3(0, 0, self.h)
		dh.y = self.w / 2
		if not self.is_in_left_side:
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
		else:
			collider_rel_center.x -= self.w / 2

		if dive_direction.y < 0:
			collider_rel_center.y += self.w / 2
		else:
			collider_rel_center.y -= self.w / 2

		self.collider_relative_position	= collider_rel_center
		self.collider = AABBCollider(self._position + self.collider_relative_position, collider_size3)
		
	def reset(self):
		self.set_default_collider()
		self.velocity = Vector3()
		