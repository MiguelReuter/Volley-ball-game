# encoding : UTF-8

import pygame as pg

from Settings import *


def check_joystick_compatibility(pg_joystick):
	"""
	Check if passed joystick is compatible for this application.

	Buttons, axes and hats number are checked to consider joystick as compatible or not.

	:param pygame.joystick.Joystick pg_joystick: joystick
	:return: True if :var pg_joystick: is compatible with current application, False else
	:rtype bool:
	"""
	if pg_joystick.get_numaxes() % 2 != 0:  # if odd, it could be a 3 axes accelerometer
		return False
	if pg_joystick.get_numbuttons() < 10:
		return False
	if pg_joystick.get_numhats() < 1:
		return False
	return True


class InputManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return InputManager.s_instance

	def __init__(self):
		InputManager.s_instance = self

		self.input_devices = []
		self.create()

	def create(self):
		pg.joystick.init()

		self.input_devices += [KeyboardInputDevice(PlayerId.PLAYER_ID_1)]

		# joystick
		for joy_id in range(pg.joystick.get_count()):
			self.add_joystick(joy_id)

	def update(self):
		joy_input_events = pg.event.get([JOYBUTTONUP, JOYBUTTONDOWN, JOYHATMOTION])
		
		for input_device in self.input_devices:
			input_device.update(joy_events=joy_input_events)
			input_device.generate_actions()

	def add_joystick(self, joy_id, player_id=None):
		"""
		Add joystick to input devices.

		:param int joy_id: pygame joystick id, must be < pygame.joystick.get_count()
		:param PlayerId enum player_id: player index to assign current joystick
		:return: None
		"""
		# check if joystick is added yet
		if self.get_joystick_by_id(joy_id) is not None:
			print("Joystick {} is added yet".format(joy_id))
			return None

		# check index validity
		if joy_id > pg.joystick.get_count() - 1:
			return None

		# add Joystick input device if joystick is compatible
		pg_joy = pg.joystick.Joystick(joy_id)
		pg_joy.init()
		if not check_joystick_compatibility(pg_joy):
			return None
		joy = JoystickInputDevice(joystick_obj=pg_joy)

		# assign joystick to a player
		if player_id in PlayerId.__iter__():
			joy.player_id = player_id

		# add joystick to input_devices
		self.input_devices += [joy]

	def assign_joystick_to_player(self, joy_id, player_id):
		device = self.get_joystick_by_id(joy_id)
		if device is None:
			print("Joystick {} does not exist in input devices")
			return

		device.player_id = player_id

	def get_joystick_by_id(self, joy_id):
		for device in self.input_devices:
			if isinstance(device, JoystickInputDevice):
				if device.joystick.get_id() == joy_id:
					return device


class InputDevice:
	def __init__(self, player_id):
		self.player_id = player_id
		self.keys = {}
		self.key_action_binds = {}

		self.input_preset = None
		
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
	
	def update(self, **kwargs):
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
		# only catch KEYUP, KEYDOWN
		for ev in pg.event.get([KEYUP, KEYDOWN]):
			if ev.type == pg.KEYDOWN:
				if ev.key in self.keys.keys():
					self.keys[ev.key] = KeyState.JUST_PRESSED
			
			if ev.type == pg.KEYUP:
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
		
		self.load_keys_and_actions_binds()


class JoystickInputDevice(InputDevice):
	def __init__(self, player_id=PlayerId.PLAYER_ID_2, joystick_obj=None):
		super().__init__(player_id)
		self.joystick = joystick_obj

		if self.joystick is not None:
			self.joystick.init()
		
		self.input_preset = INPUT_PRESET_JOYSTICK

		self.load_keys_and_actions_binds()

	def update(self, **kwargs):
		"""
		Update keys state.

		:return: None
		"""
		joy_events = kwargs["joy_events"] if "joy_events" in kwargs.keys() else []
		
		# update state
		for k in self.keys:
			if self.keys[k] == KeyState.JUST_PRESSED:
				self.keys[k] = KeyState.PRESSED
			elif self.keys[k] == KeyState.JUST_RELEASED:
				self.keys[k] = KeyState.RELEASED

		# detect a state modification (with pygame event)
		for ev in joy_events:
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
