# encoding : UTF-8

from Engine.Collisions.collider import *
import pygame as pg
from Settings import *
from ..Trajectory.trajectory_solver import *

from random import random


class CollisionsManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return CollisionsManager.s_instance

	def __init__(self):
		CollisionsManager.s_instance = self
	
	def update(self, ball, court, characters_list):
		"""
		Detect and manage collision between given objects.
		
		:param Ball ball: ball object.
		:param Court court: object used for net collision. Ball collision is checked.
		:param list(Character) characters_list: list of characters. Ball and ground collision are checked for each
		character
		:return: None
		"""
		b_refresh_target_ball_position = False
	
		# ball / ground collision
		ball.is_colliding_ground = ball.position[2] - ball.radius < 0 and ball.velocity[2] < 0
		if ball.is_colliding_ground:
			ball.velocity *= 0.7
			ball.velocity.z *= -1
			ball.position.z = max(ball.radius, ball.position.z)
			b_refresh_target_ball_position = True
		
		# ball / net collision
		ball.is_colliding_net, collision_point, ball_pos_at_collision = are_sphere_and_finite_plane_colliding(ball.collider, court.collider,
		                                                                               ball.previous_position)
		# TODO : manage tunnel collision ?
		if ball.is_colliding_net:
			# reflect velocity and set damping
			random_vect = Vector3(0, 0.1 * random(), 0)  # to prevent unstable balance
			normal_vect = Vector3(ball_pos_at_collision - collision_point + random_vect)
			ball.velocity.reflect_ip(normal_vect)
			ball.velocity *= 0.8
			
			# set ball position
			ball.position = ball_pos_at_collision
			
			b_refresh_target_ball_position = True
		
		# ball / character's collision
		ball.is_colliding_character = False
		for char in characters_list:
			char.is_colliding_ball = are_sphere_and_aabb_colliding(ball.collider, char.collider)
			
			if char.is_colliding_ball:
				ball.is_colliding_character = True
			
			# character / ground
			if char.position.z < 0:
				ground_pos = Vector3(char.position)
				ground_pos.z = 0
				char.position = ground_pos
				char.velocity.z = 0
		
		# ball velocity checked to prevent to fill event queue
		if b_refresh_target_ball_position and ball.velocity.length_squared() > 0.1:
			target_pos = find_target_position(ball.position, ball.velocity, ball.radius)
			pg.event.post(pg.event.Event(TRAJECTORY_CHANGED_EVENT, {"target_pos": target_pos}))
