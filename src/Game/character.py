# encoding : UTF-8

from pygame import *
from Engine.Display import Debug3D
from Engine.Collisions import AABBCollider
from Settings import *


from .character_states import *


class Character:
	def __init__(self, position, w=0.4, h=1, max_velocity=4):
		self._position = Vector3(position)
		self.w = w
		self.h = h
		self.collider_relative_position = Vector3(0, 0, h/2)
		self.collider = AABBCollider(self._position + self.collider_relative_position,
		                             Vector3(w, w, h))
		self.is_colliding_ball = False
		self.max_velocity = max_velocity  # m/s
		self.direction = Vector3(0, 0, 0)
		
		self.state = Idling(self)

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, value):
		self._position = value
		self.collider.center = self._position + self.collider_relative_position

	def draw(self, display_manager):
		Debug3D.draw_horizontal_ellipse(display_manager, self.position, self.w / 2)
		self.collider.draw(display_manager)

	def move_rel(self, dxyz):
		self.position += Vector3(dxyz)

	def move(self, b_up, b_down, b_left, b_RIGHT, dt):
		self.direction = Vector3(b_down - b_up, b_RIGHT - b_left, 0)
		dxyz = 0.001 * dt * self.direction * self.max_velocity
		# normalize
		if (b_up or b_down) and (b_left or b_RIGHT):
			dxyz *= 0.7071  # sqrt(2)
		self.move_rel(dxyz)
		
	def update_actions(self, action_events, dt):
		action_events = list(action_events)

		# state machine :
		# run current state
		self.state.run(action_events, dt=dt)

		# eventually switch state
		self.state = self.state.next(action_events, dt=dt)
			




