# encoding : UTF-8

import pygame as pg

from Settings import *


class InputManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return InputManager.s_instance

	def __init__(self):
		pg.joystick.init()
		self.input_devices = [KeyboardInputDevice(PlayerId.PLAYER_ID_1),
							  *[JoystickInputDevice(joystick_obj=pg.joystick.Joystick(i))
								for i in range(pg.joystick.get_count())]]

		InputManager.s_instance = self
		
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
				event = pg.event.Event(ACTION_EVENT, {"player_id": self.player_id, "action": action})
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
		for ev in pg.event.get((JOYBUTTONUP, JOYBUTTONDOWN, JOYHATMOTION)):
			if ev.joy == self.joystick.get_id():
				if ev.type == JOYBUTTONDOWN:
					if ev.button in self.keys.keys():
						self.keys[ev.button] = KeyState.JUST_PRESSED

				elif ev.type == JOYBUTTONUP:
					if ev.button in self.keys.keys():
						self.keys[ev.button] = KeyState.JUST_RELEASED

				elif ev.type == JOYHATMOTION:
					hat_id = ev.hat
					hat_value = ev.value

					for pov_i in Pov.__iter__():
						if pov_i not in self.keys.keys():
							continue

						i = 0 if pov_i.value.value[0] != 0 else 1
						b_val = pov_i.value.value[i] == hat_value[i]  # True if pov_i pressed
						b_val &= hat_id == pov_i.value.hat_id

						prev_val = self.keys[pov_i]

						if prev_val == KeyState.RELEASED and b_val:
							self.keys[pov_i] = KeyState.JUST_PRESSED
						elif prev_val == KeyState.PRESSED and not b_val:
							self.keys[pov_i] = KeyState.JUST_RELEASED

		# update joy axis states (wo pygame event)
		for axe_i in JoyAxis.__iter__():
			if axe_i not in self.keys.keys():  # check if current input_presets has an axis_i key
				continue

			axe_id = axe_i.value.axis  # axis id (usually in [0, 3] for a pad with 2 sticks)
			if axe_id < self.joystick.get_numaxes():
				needed_axe_val = axe_i.value.value
				real_axe_val = self.joystick.get_axis(axe_i.value.axis)

				b_val = axe_id == axe_i.value.axis \
						and abs(real_axe_val) > abs(needed_axe_val) \
						and real_axe_val * needed_axe_val > 0  # True if joystick axis value will send action event

				prev_val = self.keys[axe_i]

				if prev_val == KeyState.RELEASED and b_val:
					self.keys[axe_i] = KeyState.JUST_PRESSED
				elif prev_val == KeyState.PRESSED and not b_val:
					self.keys[axe_i] = KeyState.JUST_RELEASED
