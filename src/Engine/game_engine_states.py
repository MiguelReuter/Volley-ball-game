# encoding : UTF-8

import pygame as pg

import Engine.game_engine
from Engine.Trajectory import ThrowerManager
from Engine.Actions import ActionObject
from Game import CharacterStates
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
		self._pending_rule = None

		game_engine = Engine.game_engine.GameEngine.get_instance()
		self.give_service_for_character(game_engine.characters[0])
	
	def run(self, **kwargs):
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		game_engine = Engine.game_engine.GameEngine.get_instance()

		# detect rules break
		if not self.has_pending_rule():
			game_engine.ball.update_rules()

		# PHYSICS
		game_engine.ball.update_physics(dt)
		for char in game_engine.characters:
			char.update_physics(dt)
		
		# COLLISIONS
		game_engine.collisions_manager.update(game_engine.ball, game_engine.court, game_engine.characters)
		
		# KB EVENTS
		game_engine.input_manager.update()
		# AI
		game_engine.ai_manager.update()
		
		actions_events = pg.event.get(ACTION_EVENT)
		
		# UPDATE ACTIONS
		for action_object in ActionObject.objects + [self]:
			action_object.update_actions(actions_events, dt=dt)

		# throw event
		game_engine.thrower_manager.update(pg.event.get(THROW_EVENT), game_engine.ball)
		
		# manage rules
		self.update_rules(pg.event.get(RULES_BREAK_EVENT))
		
		# DISPLAY
		game_engine.display_manager.update([*game_engine.objects, game_engine.thrower_manager])
		
		# manage frame rate
		game_engine.manage_framerate_and_time()
		
	def next(self, **kwargs):
		if self._pause_requested:
			game_engine = Engine.game_engine.GameEngine.get_instance()
			game_engine.current_state = Pausing()
			self._pause_requested = False
			print("game paused")
	
	def update_actions(self, action_events, **kwargs):
		filtered_action_events = self.filter_action_events_by_player_id(action_events)
		
		for ev in filtered_action_events:
			if ev.action == PlayerAction.PAUSE:
				self._pause_requested = True
			elif ev.action == PlayerAction.SPACE_TEST:
				game_engine = Engine.game_engine.GameEngine.get_instance()
				
				# game_engine.serve(game_engine.get_character_by_player_id(ev.player_id))
				self.give_service_for_character(game_engine.get_character_by_player_id(AIId.AI_ID_1))
				# game_engine.thrower_manager.throw_ball(game_engine.ball, INITIAL_POS, TARGET_POS, WANTED_H)
				# game_engine.thrower_manager.throw_at_random_target_position(game_engine.ball, INITIAL_POS, WANTED_H)
	
	def update_rules(self, rules_break_events):
		if self.has_pending_rule():
			game_engine = Engine.game_engine.GameEngine.get_instance()
			if game_engine.get_running_ticks() - self._pending_rule.time_stamp > PENDING_RULE_DURATION:
				# give service for winner team
				winner_team = game_engine.get_winner_team_with_faulty_team_id(self._pending_rule.faulty_team)
				self.give_service_for_character(winner_team.characters[0])

				self._pending_rule = None
				return
		if ENABLE_RULES and len(rules_break_events) > 0 and not self.has_pending_rule():
			self._pending_rule = rules_break_events[-1]
			print("rule:", self._pending_rule.rule_type, "faulty team:", self._pending_rule.faulty_team, "time", self._pending_rule.time_stamp)

			# update winner team's score
			game_engine = Engine.game_engine.GameEngine.get_instance()
			game_engine.get_winner_team_with_faulty_team_id(self._pending_rule.faulty_team).score += 1

	def give_service_for_character(self, character):
		game_engine = Engine.game_engine.GameEngine.get_instance()
		
		self.reset_characters_pos_and_state()
		
		# set position and state for character
		character.position = Vector3(CHARACTER_SERVING_POS)
		if character.team.id == TeamId.LEFT:
			character.position.y *= -1
		character.state = CharacterStates.Serving(character)

		game_engine.ball.wait_to_be_served_by(character)
		ThrowerManager.get_instance().current_trajectory = None

	@staticmethod
	def reset_characters_pos_and_state():
		game_engine = Engine.game_engine.GameEngine.get_instance()
		
		for char in game_engine.characters:
			char.reset()
			
			# position
			char.position = Vector3(CHARACTER_INITIAL_POS)
			if char.team.id == TeamId.LEFT:
				char.position.y *= -1
			# state
			char.state = CharacterStates.Idling(char)

	def has_pending_rule(self):
		return self._pending_rule is not None


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
			game_engine.current_state = game_engine.running_state_instance
			print("game resumed")
	
	def update_actions(self, action_events, **kwargs):
		filtered_action_events = self.filter_action_events_by_player_id(action_events)
		
		for ev in filtered_action_events:
			if ev.action == PlayerAction.PAUSE:
				self._resume_requested = True
				

class OnMenu(GameEngineState):
	pass
