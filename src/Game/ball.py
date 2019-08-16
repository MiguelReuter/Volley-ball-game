# encoding : UTF-8

from pygame import Vector3
import pygame as pg

from Engine.Display import debug3D_utils
from Engine.Collisions import SphereCollider
from Settings.general_settings import *
import Engine


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
		
		# game rules
		self._current_team_touches = []
	
	def add_team_touch(self, character):
		team_id = character.team.id
		if len(self._current_team_touches) == 0 or self._current_team_touches[-1] != team_id:
			self._current_team_touches = [team_id]
		else:
			self._current_team_touches.append(team_id)
			if len(self._current_team_touches) > MAX_TOUCHES_NB:
				# TODO : create form in settings for dict to pass in post(Event)
				d = {"faulty_team": team_id, "rule_type": RuleType.TOUCHES_NB}
				pg.event.post(pg.event.Event(RULES_BREAK_EVENT, d))
				
	def manage_touch_ground_rule(self):
		if len(self._current_team_touches) == 0:
			faulty_team_id = None
		else:
			last_team_id = self._current_team_touches[-1]
			faulty_team_id = last_team_id
			
			# if ball pos in good area for last team --> last team wins
			game_engine = Engine.game_engine.GameEngine.get_instance()
			court = game_engine.court
			if (self.position.y < 0 and last_team_id == TeamId.RIGHT) or (self.position.y > 0 and last_team_id == TeamId.LEFT):
				if abs(self.position.x) < court.h / 2 and abs(self.position.y) < court.w / 2:
					faulty_team_id = TeamId.LEFT if last_team_id == TeamId.RIGHT else TeamId.RIGHT
		
		d = {"faulty_team": faulty_team_id, "rule_type": RuleType.GROUND}
		pg.event.post(pg.event.Event(RULES_BREAK_EVENT, d))
		
	def check_if_out_of_bounds(self):
		game_engine = Engine.game_engine.GameEngine.get_instance()
		court = game_engine.court
		if abs(self.position.x) > 1.5 * court.h / 2 or abs(self.position.y) > 1.5 * court.w / 2:
			faulty_team_id = self._current_team_touches[-1] if len(self._current_team_touches) > 0 else None
			
			d = {"faulty_team": faulty_team_id, "rule_type": RuleType.OUT_OF_BOUNDS}
			pg.event.post(pg.event.Event(RULES_BREAK_EVENT, d))
	
	def rules_reset(self):
		self._current_team_touches = []

	def wait_to_be_served_by(self, character):
		self.rules_reset()
		self.will_be_served = True
		self.position = character.get_hands_position()

	@property
	def position(self):
		return self._position
	
	@position.setter
	def position(self, value):
		self._position = value
		self.collider.center = self._position
	
	def draw_debug(self):
		prev_rect = self.rect
		prev_rect_shadow = self.rect_shadow
		
		self.rect = debug3D_utils.draw_horizontal_ellipse(Vector3(self.position[0], self.position[1], 0), self.radius)
		self.rect_shadow = self.collider.draw_debug()
		
		return [prev_rect.union(self.rect), prev_rect_shadow.union(self.rect_shadow)]
	
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
		
		self.check_if_out_of_bounds()
		
		if self.is_colliding_ground:
			self.manage_touch_ground_rule()
		
		if not self.will_be_served:
			self.add_velocity(Vector3(0, 0, -0.001 * dt * G))
			self.move_rel(0.001 * dt * self.velocity)
		else:
			self.velocity = Vector3()
