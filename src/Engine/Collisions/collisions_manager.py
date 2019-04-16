# encoding : UTF-8

from Engine.Collisions.collider import *
import pygame as pg


class CollisionsManager:
	def __init__(self, game_engine):
		self.game_engine = game_engine

	def update(self, ball, court, characters_list):
		# ball / ground collision
		ball.is_colliding_ground = ball.position[2] - ball.radius < 0 and ball.velocity[2] < 0
		if ball.is_colliding_ground:
			ball.velocity *= 0.7
			ball.velocity.z *= -1
			ball.position.z = max(ball.radius, ball.position.z)
		
		# ball / net collision
		ball.is_colliding_net = are_sphere_and_AABB_colliding(ball.collider, court.collider)
		# for tunnel collision
		if ball.previous_position.y * ball.position.y < 0 and not ball.is_colliding_net:
			dy = ball.position.y - ball.previous_position.y
			dy_center = ball.previous_position[1] / dy
			dxyz = dy_center * (ball.position - ball.previous_position).normalize()
			centered_ball_collider = SphereCollider(ball.previous_position + dxyz, ball.radius)
			ball.is_colliding_net |= are_sphere_and_AABB_colliding(centered_ball_collider, court.collider)
		# TODO : get collision point to manage bound direction
		if ball.is_colliding_net:
			ball.velocity.y *= 0.8
			ball.velocity.y *= -1
			ball.position.y = ball.previous_position.y
		
		# ball / character's collision
		ball.is_colliding_character = False
		for char in characters_list:
			if are_sphere_and_AABB_colliding(ball.collider, char.collider):
				ball.is_colliding_character = True
				char.is_colliding_ball = True
				ball.velocity = pg.Vector3(0, 0, 10)
			else:
				ball.is_colliding_character = False
				
			
		
		
