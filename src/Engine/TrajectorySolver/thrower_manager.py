# encoding : UTF-8

from pygame import *
from ..Display.Debug3D import *
from .TrajectorySolver import *
import random
from datetime import datetime
random.seed(datetime.now())


class ThrowerManager:
	def __init__(self):
		self.target_position = Vector3()
		
	def set_target_position(self):
		# target pos = court center +/- player direction +/- player position
		pass
	
	def draw(self, display_manager):
		# draw target position
		ground_pos = Vector3(self.target_position)
		ground_pos.z = 0
		draw_sphere(display_manager, self.target_position, 0.1, color=(255, 255, 0))
		draw_line(display_manager, self.target_position, ground_pos)
		
		# TODO : draw trajectory
	
	def update(self):
		pass
	
	def throw_ball(self, ball, initial_pos, target_pos, wanted_height):
		self.target_position = Vector3(target_pos)
		ball.position = Vector3(initial_pos)
		ball.velocity = find_initial_velocity(initial_pos, target_pos, wanted_height)
		
	def throw_at_random_target_position(self, ball, initial_pos, wanted_height):
		target_pos = Vector3(random.random(), random.random(), ball.radius) - (0.5, 0.5, 0)
		
		# more or less in left court side
		target_pos.x = 3 * target_pos.x
		target_pos.y = 4 * target_pos.y - 3
		
		self.target_position = target_pos
		self.throw_ball(ball, initial_pos, target_pos, wanted_height)
		
	