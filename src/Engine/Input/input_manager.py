# encoding : UTF-8

import pygame as pg

from Settings import *


class InputManager:
	# TODO : singleton
	def __init__(self, game_engine):
		# TODO : remove reference of self.keys
		self.game_engine = game_engine
		self.keys = {}
		self.key_action_bind = {}
		
		self._bind_key_to_action()
		
	def update(self):
		"""
		Update keys state.
		
		:return: None
		"""
		# update state
		for k in self.keys:
			if self.keys[k] == KeyState.JUST_PRESSED:
				self.keys[k] = KeyState.PRESSED
			elif self.keys[k] == KeyState.JUST_RELEASED:
				self.keys[k] = KeyState.RELEASED
				
		# detect a state modification (with pygame event)
		# only catch KEYUP, KEYDOWN and QUIT events
		for event in pg.event.get((pg.KEYUP, pg.KEYDOWN, pg.QUIT)):
			if event.type == pg.QUIT:
				self.game_engine.request_quit()
			if event.type == pg.KEYDOWN:
				if event.key in self.keys.keys():
					self.keys[event.key] = KeyState.JUST_PRESSED

			if event.type == pg.KEYUP:
				if event.key in self.keys.keys():
					self.keys[event.key] = KeyState.JUST_RELEASED
					
		# generate actions
		self.generate_actions()
	
	def generate_actions(self):
		"""
		Generate action events from input states.
		
		:return: None
		"""
		for (key, key_state) in self.key_action_bind:
			if self.keys[key] == key_state:
				action = self.key_action_bind[(key, key_state)]
				event = pg.event.Event(ACTIONEVENT, {'action': action})
				pg.event.post(event)
	
	def _bind_key_to_action(self):
		"""
		Bind actions and keys.
		
		Link between keys and actions are set in:
		- input_actions.py
		- input_presets.py
		
		:return: None
		"""
		
		# TODO : bind action for each connected input device (keyboard, joysticks...)
		# (key, key_state): action
		for action in INPUT_PRESET_KEYBOARD:
			key = INPUT_PRESET_KEYBOARD[action]
			self.keys[key] = KeyState.RELEASED 
			key_state = INPUT_ACTIONS[action]
			self.key_action_bind[(key, key_state)] = action
