# encoding : UTF-8

from Game.character import *
from pygame import time, event


THROW_DURATION = 500  # in ms


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
		
		b_up = b_down = b_left = b_right = False
		for act_event in action_events:
			action = act_event.action
			# move
			b_up |= (action == "MOVE_UP")
			b_down |= (action == "MOVE_DOWN")
			b_left |= (action == "MOVE_LEFT")
			b_right |= (action == "MOVE_RIGHT")
		self.character.move(b_up, b_down, b_left, b_right, dt)
	
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTIONEVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		if is_throwing_requested(action_events):
			return Throwing(self.character, action_events, **kwargs)
		
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
			# TODO : add other values to THROWEVENT ?
			event.post(event.Event(THROWEVENT, {"direction": self.character.direction,
			                                    "position": self.character.position}))
		
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
