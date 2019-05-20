# encoding : UTF-8

import pygame as pg

from Settings import *
from Game import Ball, Character, Court, CharacterStates

from Engine.Actions import ActionObject
from Engine.Collisions import CollisionsManager
from Engine.Display import DisplayManager
from Engine.AI import AIManager
from Engine.Input import InputManager
from Engine.Trajectory import ThrowerManager
import Engine.game_engine_states as GEStates


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
		self.ai_manager = AIManager()
		self.collisions_manager = CollisionsManager()
		self.display_manager = DisplayManager()
		self.input_manager = InputManager()
		self.thrower_manager = ThrowerManager()

		self.done = False
		
		self.clock = time.Clock()
		self.dt = 0
		
		self._initial_ticks = time.get_ticks()
		self._previous_ticks = self._initial_ticks
		
		self._total_ticks = 0
		self._running_ticks = 0
		self.frame_count = 0
		
		# state
		self.current_state = GEStates.Running()

		GameEngine.s_instance = self

		self._create()

	
	def _create(self):
		self.ball = Ball(INITIAL_POS, BALL_RADIUS)
		self.court = Court(COURT_DIM_Y, COURT_DIM_X, NET_HEIGHT_BTM, NET_HEIGHT_TOP)
		char1 = Character((-2, -3.5, 0), player_id=PlayerId.PLAYER_ID_1)
		#char2 = Character((0, 5, 0), player_id=PlayerId.PLAYER_ID_2, is_in_left_side=False)
		char2 = Character((0, 5, 0), player_id=PlayerId.IA_ID_1, is_in_left_side=False)
		self.characters = [char1, char2]
		self.objects = [self.court, self.ball, char1, char2]
		
		# allowed pygame events
		pg.event.set_blocked([i for i in range(pg.NUMEVENTS)])
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,
							  pg.JOYBUTTONDOWN, pg.JOYBUTTONUP,
							  pg.JOYHATMOTION,
							  pg.QUIT, pg.VIDEORESIZE,
		                      ACTION_EVENT, THROW_EVENT])

		# create
		self.ai_manager.create()

	def update_actions(self, action_events, **kwargs):
		for ev in action_events:
			if ev.action == "QUIT":
				self.request_quit()
		if len(pg.event.get(pg.QUIT)) > 0:
			self.request_quit()

	def request_quit(self):
		"""
		Call this method to quit main loop and game.
		
		:return: None
		"""
		self.done = True
	
	def serve(self, character):
		# serving position
		pos = Vector3(2, -5, 0)
		pos *= 1 if character.is_in_left_side else -1

		character.position = pos
		self.ball.will_be_served = True
		self.ball.position = character.get_hands_position()
		character.state = CharacterStates.Serving(character)
	
	def run(self):
		"""
		Main loop, call different managers (input, display...) etc.
		
		:return: None
		"""
		# ball initial velocity
		self.thrower_manager.throw_ball(self.ball, INITIAL_POS, TARGET_POS, WANTED_H)
		
		while not self.done:
			self.current_state.run(dt=self.dt)
			self.current_state.next()
			
		print("run with {} fps".format(self.get_average_fps()))

	def get_character_by_player_id(self, player_id):
		for char in self.characters:
			if char.player_id == player_id:
				return char
			
	def get_running_ticks(self):
		return self._running_ticks
	
	def get_total_ticks(self):
		return self._total_ticks
	
	def add_ticks(self, val, is_running_state):
		self._total_ticks += val
		if is_running_state:
			self._running_ticks += val
		
	def manage_framerate_and_time(self, is_running_state=True):
		t1 = self._previous_ticks
		self.clock.tick(NOMINAL_FRAME_RATE)
		t2 = pg.time.get_ticks()
		
		self.dt = TIME_SPEED * (t2 - t1)
		self.add_ticks(self.dt, is_running_state)
		self.frame_count += 1
		self._previous_ticks = t2
		
	def get_average_fps(self, ndigits=1):
		return round(1000 * self.frame_count / (time.get_ticks() - self._initial_ticks), ndigits)
	