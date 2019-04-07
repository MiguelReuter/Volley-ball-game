# encoding : UTF-8

from pygame import *
from Engine.Display import Debug3D


class Ball(sprite.Sprite):
	def __init__(self, position, radius=0.5):
		super(Ball, self).__init__()
		self.radius = radius
		self.acceleration = Vector3()
		self.velocity = Vector3()
		self.position = Vector3(position)

	def draw(self, display_manager):
		Debug3D.draw_horizontal_ellipse(display_manager.camera, (self.position[0], self.position[1], 0), self.radius)
		Debug3D.draw_sphere(display_manager.camera, self.position, self.radius)

	def move_rel(self, dxyz):
		self.position += Vector3(dxyz)
	
	def move_at(self, new_pos):
		self.position = Vector3(new_pos)
		
	def set_velocity(self, new_vel):
		self.velocity = Vector3(new_vel)
		
	def add_velocity(self, d_vel):
		self.velocity += Vector3(d_vel)
		
	def update_physics(self, dt):
		G = Vector3(0, 0, -10)
		self.add_velocity(0.001 * dt * G)
		self.move_rel(0.001 * dt * self.velocity)
		
		# if ball touches the ground
		if self.position[2] - self.radius < 0 and self.velocity[2] < 0:
			self.velocity *= 0.7
			self.velocity.z *= -1
		self.position.z = max(self.radius, self.position.z)