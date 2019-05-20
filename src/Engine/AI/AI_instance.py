# encoding : UTF-8

from pygame import Vector3
import pygame as pg
from Settings.general_settings import *
import Engine.game_engine
from Engine.Trajectory import ThrowerManager



class AIInstance:
	def __init__(self, character):
		self.character = character

	def update(self):
		game_engine = Engine.game_engine.GameEngine.get_instance()
		thrower_manager = ThrowerManager.get_instance()

		target_ball_position = thrower_manager.current_trajectory.target_pos

		if (target_ball_position.y < 0 and self.character.is_in_left_side) \
				or (target_ball_position.y > 0 and not self.character.is_in_left_side):
			target_pos = target_ball_position
		else:
			target_pos = Vector3(0, COURT_DIM_Y / 4, 0)
			target_pos.y *= -1 if self.character.is_in_left_side else 1

		self.go_to_target(target_pos)

	def go_to_target(self, target_pos):
		dx = (target_pos - self.character.position)
		thr = 0.1

		if dx.x > thr:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": self.character.player_id, "action": "MOVE_DOWN"})
			pg.event.post(ev)
		elif dx.x < -thr:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": self.character.player_id, "action": "MOVE_UP"})
			pg.event.post(ev)

		if dx.y > thr:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": self.character.player_id, "action": "MOVE_RIGHT"})
			pg.event.post(ev)
		elif dx.y < -thr:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": self.character.player_id, "action": "MOVE_LEFT"})
			pg.event.post(ev)


