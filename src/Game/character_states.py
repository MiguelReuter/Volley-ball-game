# encoding : UTF-8

from Game.character import *
from .CharacterAction import CharacterAction
from pygame import time


THROW_DURATION = 500  # in ms


class State:
	def __init__(self, character):
		self.character = character
		
	def run(self, action_events, **kwargs):
		assert 0, "run not implemented"
		
	def next(self, input, action_events, **kwargs):
		assert 0, "next not implemented"


class Idling(State):
	def run(self, action_events=None, **kwargs):
		pass
	
	def next(self, input, action_events, **kwargs):
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		
		if is_throwing_requested(action_events):
			return Throwing(self.character, action_events)
		elif is_running_requested(action_events):
			return Running(self.character, action_events, dt=dt)
		
		return self


class Running(State):
	def __init__(self, character, action_events=None, **kwargs):
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0

		super().__init__(character)
		self.run(action_events, dt=dt)
	
	def run(self, action_events, **kwargs):
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
	
	def next(self, input, action_events, **kwargs):
		if is_throwing_requested(action_events):
			return Throwing(self.character, action_events)
		
		elif not is_running_requested(action_events):
			return Idling(self.character)
		
		return self
	
	
class Throwing(State):
	def __init__(self, character, action_events=None, **kwargs):
		super().__init__(character)
		self.t0 = time.get_ticks()
		self.run(action_events, **kwargs)
	
	def run(self, action_events, **kwargs):
		if self.character.is_colliding_ball:
			# TODO : add other values to THROWEVENT ?
			event.post(event.Event(THROWEVENT, {"direction": self.character.direction,
			                                    "position": self.character.position}))
		
	def next(self, input, action_events, **kwargs):
		if time.get_ticks() - self.t0 > THROW_DURATION:
			if is_running_requested(action_events):
				return Running(self.character, action_events)
			else:
				return Idling(self.character)
		return self



def is_running_requested(action_events):
	b_running = False
	for act_event in action_events:
		b_running |= act_event.action in ("MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT")
	return b_running


def is_throwing_requested(action_events):
	b_throwing = False
	for act_event in action_events:
		b_throwing |= act_event.action == "THROW_BALL"
	return b_throwing