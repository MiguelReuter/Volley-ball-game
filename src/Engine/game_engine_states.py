# encoding : UTF-8

import Engine.game_engine
import pygame as pg

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


class Running(GameEngineState):
	def __init__(self):
		pass
	
	def run(self, **kwargs):
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		game_engine = Engine.game_engine.GameEngine.get_instance()
		
		if len(pg.event.get(pg.QUIT)) > 0:
			game_engine.request_quit()
		
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
		for action_object in ActionObject.objects:
			action_object.update_actions(actions_events, dt=dt)
		
		# throw event
		game_engine.thrower_manager.update(pg.event.get(THROW_EVENT), pg.event.get(TRAJECTORY_CHANGED_EVENT), game_engine.ball)
		
		# DISPLAY
		game_engine.display_manager.update([*game_engine.objects, game_engine.thrower_manager])
		
		# manage frame rate
		game_engine.manage_framerate_and_time()
		
	def next(self, **kwargs):
		# game_engine = Engine.game_engine.GameEngine.get_instance()
		# game_engine.current_state = self
		pass
		
		
class Pausing(GameEngineState):
	def __init__(self):
		pass
	
	def run(self, **kwargs):
		game_engine = Engine.game_engine.GameEngine.get_instance()
		
		if len(pg.event.get(pg.QUIT)) > 0:
			game_engine.request_quit()
		
		# KB EVENTS
		game_engine.input_manager.update()
		actions_events = pg.event.get(ACTION_EVENT)
		# UPDATE ACTIONS
		game_engine.update_actions(action_events=actions_events)
		
		# DISPLAY
		game_engine.display_manager.update([*game_engine.objects, game_engine.thrower_manager])
		
		# manage frame rate
		game_engine.manage_framerate_and_time()
	
	def next(self, **kwargs):
		#game_engine = Engine.game_engine.GameEngine.get_instance()
		#game_engine.current_state = self
		pass


class OnMenu(GameEngineState):
	pass


def is_paused_requested():
	pass