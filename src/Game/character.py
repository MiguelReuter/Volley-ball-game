# encoding : UTF-8

from pygame import *
from Engine.Display import Debug3D
from Engine.Collisions import AABBCollider
from Settings import *


from .character_states import *


class Character:
	def __init__(self, position, w=0.4, h=1, max_velocity=4, is_in_left_side=True):
		self._position = Vector3(position)
		self.w = w
		self.h = h
		self.collider_relative_position = Vector3(0, 0, h/2)
		self.collider = AABBCollider(self._position + self.collider_relative_position,
		                             Vector3(w, w, h))
		self.is_colliding_ball = False
		self.max_velocity = max_velocity  # m/s
		self.velocity = Vector3()
		self.direction = Vector3()
		
		self.is_in_left_side = is_in_left_side
		
		self.state = Idling(self)

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, value):
		self._position = value
		self.collider.center = self._position + self.collider_relative_position

	def draw(self, display_manager):
		ground_pos = Vector3(self.position)
		ground_pos.z = 0
		Debug3D.draw_horizontal_ellipse(display_manager, ground_pos, self.w / 2)
		self.collider.draw(display_manager)

	def move_rel(self, dxyz):
		self.position += Vector3(dxyz)

	def move(self, direction, dt):
		dxyz = 0.001 * dt * direction * self.max_velocity
		self.move_rel(dxyz)
		
	def update_actions(self, action_events, dt):
		action_events = list(action_events)

		# state machine :
		# run current state
		self.state.run(action_events, dt=dt)

		# eventually switch state
		self.state = self.state.next(action_events, dt=dt)
		
	def get_hands_position(self):
		dh = Vector3(0, 0, self.h)
		dh.y = self.w / 2
		if not self.is_in_left_side:
			dh.y *= -1
		return self.position + dh



