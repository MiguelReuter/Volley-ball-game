# encoding : UTF-8

import pygame as pg

import Engine.game_engine
from Engine.Actions import ActionObject
from Settings import *


class GameEngineState:
	"""
	Virtual class for game engine's state.
	"""
	
	def __init__(self):
		pass
	
	def run(self, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param kwargs: some parameters
		:return: None
		"""
		assert 0, "run not implemented"
	
	def next(self, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param kwargs: some parameters
		:return a state
		:rtype State:
		"""
		assert 0, "next not implemented"


class OnCreation(GameEngineState):
	pass


class Running(GameEngineState, ActionObject):
	def __init__(self):
		ActionObject.__init__(self, add_to_objects_list=False)
		self._pause_requested = False
	
	def run(self, **kwargs):
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		game_engine = Engine.game_engine.GameEngine.get_instance()
		
		# PHYSICS
		game_engine.ball.update_physics(dt)
		for char in [game_engine.char1, game_engine.char2]:
			char.update_physics(dt)
		
		# COLLISIONS
		game_engine.collisions_manager.update(game_engine.ball, game_engine.court,
		                                      [game_engine.char1, game_engine.char2])
		
		# KB EVENTS
		game_engine.input_manager.update()
		actions_events = pg.event.get(ACTION_EVENT)
		# UPDATE ACTIONS
		for action_object in ActionObject.objects + [self]:
			action_object.update_actions(actions_events, dt=dt)
		
		# throw event
		game_engine.thrower_manager.update(pg.event.get(THROW_EVENT), game_engine.ball)
		
		# DISPLAY
		game_engine.display_manager.update([*game_engine.objects, game_engine.thrower_manager])
		
		# manage frame rate
		game_engine.manage_framerate_and_time()
		
	def next(self, **kwargs):
		if self._pause_requested:
			game_engine = Engine.game_engine.GameEngine.get_instance()
			game_engine.current_state = Pausing()
			print("game paused")
	
	def update_actions(self, action_events, **kwargs):
		filtered_action_events = self.filter_action_events_by_player_id(action_events)
		
		for ev in filtered_action_events:
			if ev.action == "PAUSE":
				self._pause_requested = True
			elif ev.action == "SPACE_TEST":
				game_engine = Engine.game_engine.GameEngine.get_instance()
				
				game_engine.serve(game_engine.get_character_by_player_id(ev.player_id))
				# game_engine.thrower_manager.throw_ball(game_engine.ball, INITIAL_POS, TARGET_POS, WANTED_H)
				# game_engine.thrower_manager.throw_at_random_target_position(game_engine.ball, INITIAL_POS, WANTED_H)
	
	
class Pausing(GameEngineState, ActionObject):
	def __init__(self):
		ActionObject.__init__(self, add_to_objects_list=False)
		self._resume_requested = False
	
	def run(self, **kwargs):
		game_engine = Engine.game_engine.GameEngine.get_instance()
		
		# KB EVENTS
		game_engine.input_manager.update()
		actions_events = pg.event.get(ACTION_EVENT)
		# UPDATE ACTIONS
		self.update_actions(action_events=actions_events)
		game_engine.update_actions(action_events=actions_events)
		
		# DISPLAY
		game_engine.display_manager.update([*game_engine.objects, game_engine.thrower_manager])
		
		# manage frame rate
		game_engine.manage_framerate_and_time(is_running_state=False)
	
	def next(self, **kwargs):
		if self._resume_requested:
			game_engine = Engine.game_engine.GameEngine.get_instance()
			game_engine.current_state = Running()
			print("game resumed")
	
	def update_actions(self, action_events, **kwargs):
		filtered_action_events = self.filter_action_events_by_player_id(action_events)
		
		for ev in filtered_action_events:
			if ev.action == "PAUSE":
				self._resume_requested = True
				

class OnMenu(GameEngineState):
	pass
