# encoding : UTF-8

import pygame as pg

from Settings import *
from Game import Ball, Team, Character, Court, CharacterStates

from Engine.Actions import ActionObject
from Engine.AI.ai_manager import AIManager
from Engine.Collisions import CollisionsManager
from Engine.Display import DisplayManager
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
		GameEngine.s_instance = self

		ActionObject.__init__(self)
		self.ai_manager = AIManager()
		self.display_manager = DisplayManager()
		self.input_manager = InputManager()
		self.collisions_manager = CollisionsManager()
		self.thrower_manager = ThrowerManager()

		self.done = False

		self.clock = time.Clock()
		self.dt = 0

		self._initial_ticks = time.get_ticks()
		self._previous_ticks = self._initial_ticks

		self._total_ticks = 0
		self._running_ticks = 0
		self.frame_count = 0

		# game objects
		self.ball = None
		self.court = None
		self.characters = []
		self.teams = {}

		# states
		self._states = {}
		self._current_state_type = None

		self._create()

	def _create(self):
		# allowed pygame events
		pg.event.set_blocked([i for i in range(pg.NUMEVENTS)])
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP,
							  pg.JOYBUTTONDOWN, pg.JOYBUTTONUP,
							  pg.JOYHATMOTION,
							  pg.QUIT, pg.VIDEORESIZE,
		                      ACTION_EVENT, THROW_EVENT, RULES_BREAK_EVENT])

		self.new_game([PlayerId.PLAYER_ID_1, AIId.AI_ID_1])

		# states
		self._states[GEStateType.RUNNING] = GEStates.Running()
		self._states[GEStateType.PAUSING] = GEStates.Pausing()

		self._current_state_type = GEStateType.RUNNING

	def set_current_state_type(self, state_type):
		if state_type in self._states.keys():
			self._current_state_type = state_type
		else:
			print("GEStateType {} not in self._states".format(state_type))

	def get_current_state(self):
		return self._states[self._current_state_type]

	def new_game(self, player_id_list=None):
		self.ai_manager.reset()
		
		player_id_list = player_id_list if player_id_list is not None else [AIId.AI_ID_1, AIId.AI_ID_2]
		self.ball = Ball(radius=BALL_RADIUS)
		self.court = Court(COURT_DIM_Y, COURT_DIM_X, NET_HEIGHT_BTM, NET_HEIGHT_TOP)
		self.characters = []

		for pl_id in player_id_list:
			char = Character(player_id=pl_id)
			self.characters.append(char)
			# AI
			if pl_id in AIId.__iter__():
				self.ai_manager.add_entity(char)

		self.objects = [self.court, self.ball] + self.characters

		# teams
		l_char = self.characters[0:len(self.characters)//2]
		l_team = Team(characters_list=l_char, team_id=TeamId.LEFT)

		r_char = self.characters[len(self.characters)//2:]
		r_team = Team(characters_list=r_char, team_id=TeamId.RIGHT)

		self.teams = {TeamId.LEFT: l_team, TeamId.RIGHT: r_team}

	def update_actions(self, action_events, **kwargs):
		for ev in action_events:
			if ev.action == PlayerAction.QUIT:
				self.request_quit()
		if len(pg.event.get(pg.QUIT)) > 0:
			self.request_quit()

	def request_quit(self):
		"""
		Call this method to quit main loop and game.
		
		:return: None
		"""
		self.done = True

	def run(self):
		"""
		Main loop, call different managers (input, display...) etc.
		
		:return: None
		"""
		while not self.done:
			current_state = self._states[self._current_state_type]
			current_state.run(dt=self.dt)
			current_state.next()

		print("run with {} fps".format(self.get_average_fps()))

	def get_character_by_player_id(self, player_id):
		for char in self.characters:
			if char.player_id == player_id:
				return char

	def get_winner_team_with_faulty_team_id(self, faulty_team_id):
		winner_team_id = TeamId.LEFT if faulty_team_id == TeamId.RIGHT else TeamId.RIGHT
		return self.teams[winner_team_id]

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
	