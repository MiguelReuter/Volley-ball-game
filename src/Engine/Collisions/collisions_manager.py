# encoding : UTF-8

from Engine.Collisions.collider import *
import pygame as pg
from settings import *
from ..TrajectorySolver.TrajectorySolver import *


class CollisionsManager:
	def __init__(self, game_engine):
		self.game_engine = game_engine

	def update(self, ball, court, characters_list):
		b_refresh_target_ball_position = False
		
		# ball / ground collision
		ball.is_colliding_ground = ball.position[2] - ball.radius < 0 and ball.velocity[2] < 0
		if ball.is_colliding_ground:
			ball.velocity *= 0.7
			ball.velocity.z *= -1
			ball.position.z = max(ball.radius, ball.position.z)
			b_refresh_target_ball_position = True
		
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
			b_refresh_target_ball_position = True
		
		# ball / character's collision
		ball.is_colliding_character = False
		for char in characters_list:
			char.is_colliding_ball = are_sphere_and_AABB_colliding(ball.collider, char.collider)
			
			if char.is_colliding_ball:
				ball.is_colliding_character = True
				
		# ball velocity checked to prevent to fill event queue
		if b_refresh_target_ball_position and ball.velocity.length_squared() > 0.1:
			target_pos = find_target_position(ball.position, ball.velocity, ball.radius)
			pg.event.post(pg.event.Event(TRAJECTORY_CHANGED_EVENT, {"target_pos": target_pos}))