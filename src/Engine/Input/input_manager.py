# encoding : UTF-8

import pygame as pg

from Settings import *


class InputManager:
	# TODO : singleton
	def __init__(self, game_engine):
		pg.joystick.init()
		self.game_engine = game_engine
		self.input_devices = [KeyboardInputDevice(PlayerId.PLAYER_ID_1),
							  *[JoystickInputDevice(joystick_obj=joystick.Joystick(i))
								for i in range(joystick.get_count())]]
		
	def update(self):
		for input_device in self.input_devices:
			input_device.update()
			input_device.generate_actions()
			

class InputDevice:
	def __init__(self, player_id):
		self.player_id = player_id
		self.keys = {}
		self.key_action_binds = {}

		self.input_preset = None
		self.up_input_event = None
		self.down_input_event = None
		
	def load_keys_and_actions_binds(self):
		self.keys = {}
		self.key_action_binds = {}
		
		assert self.input_preset is not None
		
		# (key, key_state): action
		for action in self.input_preset:
			key = self.input_preset[action]
			self.keys[key] = KeyState.RELEASED
			key_state = INPUT_ACTIONS[action]
			self.key_action_binds[(key, key_state)] = action
	
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
		for ev in pg.event.get((self.up_input_event, self.down_input_event)):
			if ev.type == self.down_input_event:
				if ev.key in self.keys.keys():
					self.keys[ev.key] = KeyState.JUST_PRESSED
			
			if ev.type == self.up_input_event:
				if ev.key in self.keys.keys():
					self.keys[ev.key] = KeyState.JUST_RELEASED
	
	def generate_actions(self):
		"""
		Generate action events from input states.

		:return: None
		"""
		for (key, key_state) in self.key_action_binds:
			if self.keys[key] == key_state:
				action = self.key_action_binds[(key, key_state)]
				event = pg.event.Event(ACTION_EVENT, {'player_id': self.player_id,
				                                     'action': action})
				pg.event.post(event)
		

class KeyboardInputDevice(InputDevice):
	def __init__(self, player_id=PlayerId.PLAYER_ID_1):
		super().__init__(player_id)
		self.input_preset = INPUT_PRESET_KEYBOARD
		self.up_input_event = pg.KEYUP
		self.down_input_event = pg.KEYDOWN
		
		self.load_keys_and_actions_binds()


class JoystickInputDevice(InputDevice):
	def __init__(self, player_id=PlayerId.PLAYER_ID_2, joystick_obj=None):
		super().__init__(player_id)
		self.joystick = joystick_obj

		if self.joystick is not None:
			self.joystick.init()
		
		self.input_preset = INPUT_PRESET_JOYSTICK
		self.up_input_event = pg.JOYBUTTONUP
		self.down_input_event = pg.JOYBUTTONDOWN

		self.load_keys_and_actions_binds()

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
		for ev in pg.event.get((JOYBUTTONUP, JOYBUTTONDOWN)):
			if ev.type == JOYBUTTONDOWN:
				if ev.button in self.keys.keys():
					self.keys[ev.button] = KeyState.JUST_PRESSED

			if ev.type == JOYBUTTONUP:
				if ev.button in self.keys.keys():
					self.keys[ev.button] = KeyState.JUST_RELEASED

	def generate_actions(self):
		super().generate_actions()

		for input_id, input_state in self.key_action_binds:
			# hat
			if isinstance(input_id, JoyHat):
				hat_id = input_id.hat_id
				value = input_id.value

				if hat_id < self.joystick.get_numhats():
					hat_x, hat_y = self.joystick.get_hat(hat_id)
					if (hat_x != 0 and hat_x == value[0]) or (hat_y != 0 and hat_y == value[1]):
						action = self.key_action_binds[(input_id, input_state)]
						ev = pg.event.Event(ACTION_EVENT, {'player_id': self.player_id,
															  'action': action})
						pg.event.post(ev)
			# axis
			if isinstance(input_id, JoyAxis):
				axis = input_id.axis
				value = input_id.value

				if axis < self.joystick.get_numaxes():
					axis_val = self.joystick.get_axis(axis)
					if abs(axis_val) > abs(value) and axis_val * value > 0:
						action = self.key_action_binds[(input_id, input_state)]
						ev = pg.event.Event(ACTION_EVENT, {'player_id': self.player_id,
														   'action': action})
						pg.event.post(ev)

