# encoding : UTF-8

from pygame import Vector3
import pygame as pg

from Engine.Display import debug3D_utils
from Engine.Collisions import SphereCollider
from Settings import G


class Ball(pg.sprite.DirtySprite):
	def __init__(self, position, radius=0.5, sprite_groups=[]):
		pg.sprite.DirtySprite.__init__(self, *sprite_groups)
		self.radius = radius
		self.acceleration = Vector3()
		self.velocity = Vector3()
		self._position = Vector3(position)
		self.previous_position = Vector3(position)
		self.collider = SphereCollider(position, radius)
		
		self.is_colliding_ground = False
		self.is_colliding_net = False
		self.is_colliding_character = False
		
		self.will_be_served = False
		
		# sprite
		self.rect_shadow = pg.Rect(0, 0, 0, 0)
		self.rect = pg.Rect(0, 0, 0, 0)
	
	@property
	def position(self):
		return self._position
	
	@position.setter
	def position(self, value):
		self._position = value
		self.collider.center = self._position
	
	def draw(self):
		prev_ball_rect = self.rect
		prev_shadow_rect = self.rect_shadow
		
		self.rect = debug3D_utils.draw_horizontal_ellipse(Vector3(self.position[0], self.position[1], 0), self.radius)
		self.rect_shadow = self.collider.draw()
		
		return [pg.Rect(0, 0, 0, 0).unionall([prev_shadow_rect, self.rect_shadow]),
		        pg.Rect(0, 0, 0, 0).unionall([prev_ball_rect, self.rect])]
	
	def move_rel(self, dxyz):
		self.position += Vector3(dxyz)
	
	def move_at(self, new_pos):
		self.position = Vector3(new_pos)
	
	def set_velocity(self, new_vel):
		self.velocity = Vector3(new_vel)
	
	def add_velocity(self, d_vel):
		self.velocity += Vector3(d_vel)
	
	def update_physics(self, dt):
		self.previous_position = Vector3(self.position)
		
		if not self.will_be_served:
			self.add_velocity(Vector3(0, 0, -0.001 * dt * G))
			self.move_rel(0.001 * dt * self.velocity)
		else:
			self.velocity = Vector3()
