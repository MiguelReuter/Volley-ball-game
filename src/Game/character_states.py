# encoding : UTF-8

from Game.character import *
from pygame import time, event

from Settings import G, THROW_DURATION, JUMP_VELOCITY


class State:
	"""
	Virtual class for character's state.
	"""
	def __init__(self, character):
		"""
		:param Character character: character which state is attached to
		"""
		self.character = character
		
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		assert 0, "run not implemented"
		
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		assert 0, "next not implemented"


class Idling(State):
	"""
	Character state for idling.
	"""
	def run(self, action_events=None, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		pass
	
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay at same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters :
			- :var float dt: time between 2 function calls
		:return a state
		:rtype State:
		"""
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		
		if is_throwing_requested(action_events):
			return Throwing(self.character, action_events)
		elif is_jumping_requested(action_events):
			return Jumping(self.character, action_events, dt=dt)
		elif is_running_requested(action_events):
			return Running(self.character, action_events, dt=dt)
		
		return self


class Running(State):
	"""
	Character state for running.
	"""
	def __init__(self, character, action_events=None, **kwargs):
		"""
		:param Character character: character which state is attached to
		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters :
			- :var float dt: time between 2 function calls
		"""
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0

		super().__init__(character)
		self.run(action_events, dt=dt)  # to prevent delay, run is directly called here
	
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters :
			- :var float dt: time between 2 function calls
		"""
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		direction = get_normalized_direction_requested(action_events)
		self.character.move(direction, dt)
	
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		
		if is_throwing_requested(action_events):
			return Throwing(self.character, action_events, **kwargs)
		elif is_jumping_requested(action_events):
			return Jumping(self.character, action_events, dt=dt)
		elif not is_running_requested(action_events):
			return Idling(self.character)
		
		return self
	
	
class Throwing(State):
	"""
	Character state for throwing a ball
	"""
	def __init__(self, character, action_events=None, **kwargs):
		super().__init__(character)
		self.t0 = time.get_ticks()
		self.run(action_events, **kwargs)
	
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		if self.character.is_colliding_ball:
			# throwing velocity efficiency
			vel_eff = get_velocity_efficiency(time.get_ticks() - self.t0)
			
			direction = get_normalized_direction_requested(action_events)
			# TODO : add other values to THROWEVENT ?
			event.post(event.Event(THROWEVENT, {"direction": direction,
			                                    "position": self.character.position,
			                                    "velocity_efficiency": vel_eff}))
		
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		if time.get_ticks() - self.t0 > THROW_DURATION:
			if is_running_requested(action_events):
				return Running(self.character, action_events, **kwargs)
			else:
				return Idling(self.character)
		return self


class Jumping(State):
	"""
	Character state for jumping
	"""
	
	def __init__(self, character, action_events=None, **kwargs):
		super().__init__(character)
		self.character.velocity = Vector3(0, 0, JUMP_VELOCITY)
	
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0

		self.character.velocity += Vector3(0, 0, -0.001 * dt * G)
		self.character.move_rel(0.001 * dt * self.character.velocity)
	
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		
		# player touches ground
		if self.character.position.z <= 0:
			self.character.position.z = 0
			return Idling(self.character)
		return self


def is_running_requested(action_events):
	"""
	Return true if running action is requested.

	:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
	:return: True if running action is requested
	:rtype bool:
	"""
	b_running = False
	for act_event in action_events:
		b_running |= act_event.action in ("MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT")
	return b_running


def is_throwing_requested(action_events):
	"""
	Return true if throwing action is requested.

	:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
	:return: True if throwing action is requested
	:rtype bool:
	"""
	b_throwing = False
	for act_event in action_events:
		b_throwing |= act_event.action == "THROW_BALL"
	return b_throwing


def is_jumping_requested(action_events):
	"""
	Return true if jumping action is requested.

	:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
	:return: True if jumping action is requested
	:rtype bool:
	"""
	b_jumping = False
	for act_event in action_events:
		b_jumping |= act_event.action == "JUMP"
	return b_jumping


def get_normalized_direction_requested(action_events):
	b_up = b_down = b_left = b_right = False
	for act_event in action_events:
		action = act_event.action
		b_up |= (action == "MOVE_UP")
		b_down |= (action == "MOVE_DOWN")
		b_left |= (action == "MOVE_LEFT")
		b_right |= (action == "MOVE_RIGHT")
	
	direction = Vector3(b_down - b_up, b_right - b_left, 0)
	
	# normalize
	if (b_left | b_right) & (b_up | b_down):
		direction *= 0.7071
		
	return direction


def get_velocity_efficiency(dt, period=THROW_DURATION):
	"""
	Process and return throwing velocity efficiency.
	
	Efficiency is maximum when character hits the ball at the moment when he touch the ball (not too early).
	
	:param int dt: time in ms between throw request and effective throw, i.e. when payer touches the ball
	:param int period: duration of throwing. :var dt: / :var period: will be used to process velocity efficiency
	:return: throwing velocity efficiency in [0, 1]
	:rtype float:
	"""
	# some parameters
	thr = 0.4
	a = 0.8
	
	x = dt / period  # x in [0, 1]
	y = 1 if x < thr else 1 - a * x + thr
	return y
