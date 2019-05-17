# encoding : UTF-8

from .Display import *
from .Input import *

from Settings import *
from Game.ball import Ball
from Game.court import Court
from Game.character import Character
from Game.character_states import *

from Engine.Collisions import *
from .TrajectorySolver import ThrowerManager

from Engine.Actions import ActionObject

import Engine.game_engine_states as GEStates

import pygame as pg


INITIAL_POS = pg.Vector3(-2, 5, 1)
TARGET_POS = pg.Vector3(-2, -3, 0.5)
WANTED_H = 4


class GameEngine(ActionObject):
	s_instance = None

	@staticmethod
	def get_instance():
		return GameEngine.s_instance

	def __init__(self):
		ActionObject.__init__(self)
		self.display_manager = DisplayManager()
		self.input_manager = InputManager()
		self.collisions_manager = CollisionsManager()
		self.thrower_manager = ThrowerManager()

		self.running = True
		
		self.initial_ticks = time.get_ticks()
		self.clock = time.Clock()
		self.dt = 0
		self.previous_ticks = self.initial_ticks
		self._ticks_since_init = 0
		self.frame_count = 0
		
		# states
		self.paused = False
		
		self.running_state = GEStates.Running()
		self.pausing_state = GEStates.Pausing()
		self.current_state = self.running_state
		
		self._create()

		GameEngine.s_instance = self
	
	def _create(self):
		self.ball = Ball(INITIAL_POS, BALL_RADIUS)
		self.court = Court(COURT_DIM_Y, COURT_DIM_X, NET_HEIGHT_BTM, NET_HEIGHT_TOP)
		self.char1 = Character((-2, -3.5, 0), player_id=PlayerId.PLAYER_ID_1)
		self.char2 = Character((0, 5, 0), player_id=PlayerId.PLAYER_ID_2, is_in_left_side=False)
		self.objects = [self.court, self.ball, self.char1, self.char2]
		
		# allowed pygame events
		pg.event.set_blocked([i for i in range(pg.NUMEVENTS)])
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,
							  pg.JOYBUTTONDOWN, pg.JOYBUTTONUP,
							  pg.JOYHATMOTION,
							  pg.QUIT, pg.VIDEORESIZE,
		                      ACTION_EVENT, THROW_EVENT, TRAJECTORY_CHANGED_EVENT])

	def request_quit(self):
		"""
		Call this method to quit main loop and game.
		
		:return: None
		"""
		self.running = False
	
	def serve(self, character):
		# serving position
		pos = Vector3(2, -5, 0)
		pos *= 1 if character.is_in_left_side else -1

		character.position = pos
		self.ball.will_be_served = True
		self.ball.position = character.get_hands_position()
		character.state = Serving(character)
	
	def update_actions(self, action_events, **kwargs):
		filtered_action_events = self.filter_action_events_by_player_id(action_events)
		# TODO: add an update_actions method in each GameEngine States ?
		for ev in filtered_action_events:
			action = ev.action
			if action == "QUIT":
				self.running = False
			elif action == "PAUSE":
				if self.current_state == self.pausing_state:
					self.current_state = self.running_state
				elif self.current_state == self.running_state:
					self.current_state = self.pausing_state
			elif action == "SPACE_TEST":
				# TODO : bugfix - we can request a service on a paused game
				self.serve(self.get_character_by_player_id(ev.player_id))
				#self.thrower_manager.throw_ball(self.ball, INITIAL_POS, TARGET_POS, WANTED_H)
				#self.thrower_manager.throw_at_random_target_position(self.ball, INITIAL_POS, WANTED_H)
		
	def run(self):
		"""
		Main loop, call different managers (input, display...) etc.
		
		:return: None
		"""
		# ball initial velocity
		self.thrower_manager.throw_ball(self.ball, INITIAL_POS, TARGET_POS, WANTED_H)
		
		while self.running:
			self.current_state.run(dt=self.dt)
			self.current_state.next()
			
		print("run with {} fps".format(self.get_average_fps()))

	def get_character_by_player_id(self, player_id):
		for char in (self.char1, self.char2):
			if char.player_id == player_id:
				return char
			
	def get_ticks_since_init(self):
		return self._ticks_since_init
	
	def add_ticks(self, val):
		self._ticks_since_init += val
		
	def manage_framerate_and_time(self):
		t1 = self.previous_ticks
		self.clock.tick(NOMINAL_FRAME_RATE)
		t2 = pg.time.get_ticks()
		
		self.dt = TIME_SPEED * (t2 - t1)
		self.add_ticks(self.dt)
		self.frame_count += 1
		self.previous_ticks = t2
		
	def get_average_fps(self, ndigits=1):
		return round(1000 * self.frame_count / (time.get_ticks() - self.initial_ticks), ndigits)
	