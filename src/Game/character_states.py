# encoding : UTF-8

import Engine.game_engine
from Settings import *


class CharacterState:
	"""
	Virtual class for character's state.
	"""
	def __init__(self, character):
		"""
		:param Character character: character which state is attached to
		"""
		self.character = character
		self.character.velocity = Vector3()
		
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		assert 0, "run not implemented"
		
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		assert 0, "next not implemented"


class Idling(CharacterState):
	"""
	Character state for idling.
	"""
	def run(self, action_events=None, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		pass
	
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay at same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
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
		elif is_diving_requested(action_events):
			return Diving(self.character, action_events)
		elif is_running_requested(action_events):
			return Running(self.character, action_events, dt=dt)
		return self


class Running(CharacterState):
	"""
	Character state for running.
	"""
	def __init__(self, character, action_events=None, **kwargs):
		"""
		:param Character character: character which state is attached to
		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters :
			- :var float dt: time between 2 function calls
		"""
		if action_events is None:
			action_events = []
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0

		super().__init__(character)
		self.run(action_events, dt=dt)  # to prevent delay, run is directly called here
	
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters :
			- :var float dt: time between 2 function calls
		"""
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		direction = get_normalized_direction_requested(action_events)
		self.character.move(direction, dt)
	
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		dt = kwargs["dt"] if "dt" in kwargs.keys() else 0
		
		if is_throwing_requested(action_events):
			return Throwing(self.character, action_events, **kwargs)
		elif is_jumping_requested(action_events):
			return Jumping(self.character, action_events, dt=dt)
		elif is_diving_requested(action_events):
			return Diving(self.character, action_events)
		elif not is_running_requested(action_events):
			return Idling(self.character)
		
		return self
	
	
class Throwing(CharacterState):
	"""
	Character state for throwing a ball
	"""
	def __init__(self, character, action_events=None, **kwargs):
		super().__init__(character)
		self.t0 = Engine.game_engine.GameEngine.get_instance().get_running_ticks()
		self.has_thrown_yet = False

		if action_events is None:
			action_events = []
		self.run(action_events, **kwargs)
	
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		if self.character.is_colliding_ball and not self.has_thrown_yet:
			self.has_thrown_yet = True
			# throwing velocity efficiency
			vel_eff = get_velocity_efficiency(Engine.game_engine.GameEngine.get_instance().get_running_ticks() - self.t0)
			
			direction = get_direction_requested(action_events)
			event.post(event.Event(THROW_EVENT, {"throwing_type": ThrowingType.THROW,
			                                     "character": self.character,
			                                     "direction": direction,
			                                     "position": self.character.position,
			                                     "velocity_efficiency": vel_eff}))
		
	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		if Engine.game_engine.GameEngine.get_instance().get_running_ticks() - self.t0 > THROW_DURATION:
			if is_running_requested(action_events):
				return Running(self.character, action_events, **kwargs)
			else:
				return Idling(self.character)
		return self


class Serving(CharacterState):
	"""
	Character state for serving a ball
	"""
	def __init__(self, character, action_events=None, **kwargs):
		super().__init__(character)
		character.reset()
		
		self.has_served = False
		if action_events is None:
			action_events = []
		self.run(action_events, **kwargs)
		
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		
		if is_throwing_requested(action_events) and not self.has_served:
			self.t0 = Engine.game_engine.GameEngine.get_instance().get_running_ticks()
			self.has_served = True
			direction = get_direction_requested(action_events)
			event.post(event.Event(THROW_EVENT, {"throwing_type": ThrowingType.SERVE,
			                                     "character": self.character,
			                                     "direction": direction,
			                                     "position": self.character.position}))

	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		if self.has_served and Engine.game_engine.GameEngine.get_instance().get_running_ticks() - self.t0 > SERVE_DURATION:
			if is_running_requested(action_events):
				return Running(self.character, action_events, **kwargs)
			else:
				return Idling(self.character)
		return self


class Jumping(CharacterState):
	"""
	Character state for jumping
	"""
	
	def __init__(self, character, action_events=None, **kwargs):
		super().__init__(character)
		self.character.velocity = Vector3(0, 0, JUMP_VELOCITY)
		self.has_smashed = False
	
	def run(self, action_events, **kwargs):
		"""
		Main function for this state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return: None
		"""
		if self.character.is_colliding_ball and is_throwing_requested(action_events) and not self.has_smashed:
			self.has_smashed = True
			direction = get_direction_requested(action_events)
			event.post(event.Event(THROW_EVENT, {"throwing_type": ThrowingType.SMASH,
			                                     "character": self.character,
			                                     "direction": direction,
			                                     "position": self.character.position}))

	def next(self, action_events, **kwargs):
		"""
		Function called to change (or stay same) state, usually called at each frame.

		:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
		:param kwargs: some other parameters
		:return a state
		:rtype State:
		"""
		
		# player touches ground
		if self.character.position.z <= 0:
			ground_pos = Vector3(self.character.position)
			ground_pos.z = 0
			self.character.position = ground_pos
			return Idling(self.character)
		return self


class Diving(CharacterState):
	"""
	Character state for diving
	"""

	def __init__(self, character, action_events=None, **kwargs):
		CharacterState.__init__(self, character)
		self.t0 = Engine.game_engine.GameEngine.get_instance().get_running_ticks()
		self.has_touch_ball = False
		if action_events is None:
			action_events = []

		direction = get_normalized_direction_requested(action_events)
		if direction.x == 0 and direction.y == 0:
			direction.y = 1 if self.character.is_in_left_side else -1

		self.character.velocity = DIVE_SPEED * direction
		self.character.set_diving_collider(direction)

	def run(self, action_events, **kwargs):
		if Engine.game_engine.GameEngine.get_instance().get_running_ticks() - self.t0 > DIVE_SLIDE_DURATION:
			self.character.velocity = Vector3()

		if self.character.is_colliding_ball and not self.has_touch_ball:
			self.has_touch_ball = True
			TOTAL_DURATION = DIVE_SLIDE_DURATION + DIVE_DURATION_FOR_STANDING_UP

			x = (Engine.game_engine.GameEngine.get_instance().get_running_ticks() - self.t0) / TOTAL_DURATION

			thr = DIVE_SLIDE_DURATION / TOTAL_DURATION
			alpha = TOTAL_DURATION / DIVE_DURATION_FOR_STANDING_UP
			vel_eff = 1.0 if x < thr else 1.0 - alpha * (x - thr)

			event.post(event.Event(THROW_EVENT, {"throwing_type": ThrowingType.DRAFT,
			                                     "character": self.character,
			                                     "direction": get_normalized_direction_requested(action_events),
			                                     "position": self.character.position,
												 "velocity_efficiency": vel_eff}))

	def next(self, action_events, **kwargs):
		if Engine.game_engine.GameEngine.get_instance().get_running_ticks() - self.t0 \
				> DIVE_SLIDE_DURATION + DIVE_DURATION_FOR_STANDING_UP:
			self.character.set_default_collider()

			# change state
			if is_running_requested(action_events):
				return Running(self.character, action_events, **kwargs)
			else:
				return Idling(self.character)
		return self


def is_running_requested(action_events):
	"""
	Return true if running action is requested.

	:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
	:return: True if running action is requested
	:rtype bool:
	"""
	b_running = False
	for act_event in action_events:
		b_running |= act_event.action in (PlayerAction.MOVE_LEFT, PlayerAction.MOVE_RIGHT, PlayerAction.MOVE_UP, PlayerAction.MOVE_DOWN)
	return b_running


def is_throwing_requested(action_events):
	"""
	Return true if throwing action is requested.

	:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
	:return: True if throwing action is requested
	:rtype bool:
	"""
	b_throwing = False
	for act_event in action_events:
		b_throwing |= act_event.action == PlayerAction.THROW_BALL
	return b_throwing


def is_jumping_requested(action_events):
	"""
	Return true if jumping action is requested.

	:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
	:return: True if jumping action is requested
	:rtype bool:
	"""
	b_jumping = False
	for act_event in action_events:
		b_jumping |= act_event.action == PlayerAction.JUMP
	return b_jumping


def is_diving_requested(action_events):
	"""
	Return true if diving action is requested.

	:param list[pygame.event.Event(ACTION_EVENT)] action_events: list of action events
	:return: True if diving action is requested
	:rtype bool:
	"""
	b_diving = False
	for act_event in action_events:
		b_diving |= act_event.action == PlayerAction.DIVE
	return b_diving


def get_direction_requested(action_events):
	b_up = b_down = b_left = b_right = False
	for act_event in action_events:
		action = act_event.action
		b_up |= (action == PlayerAction.MOVE_UP)
		b_down |= (action == PlayerAction.MOVE_DOWN)
		b_left |= (action == PlayerAction.MOVE_LEFT)
		b_right |= (action == PlayerAction.MOVE_RIGHT)
	
	return Vector3(b_down - b_up, b_right - b_left, 0)


def get_normalized_direction_requested(action_events):
	direction = get_direction_requested(action_events)
	
	# normalize
	if abs(direction[0]) + abs(direction[1]) == 2:
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
