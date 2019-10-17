# encoding : UTF-8

from Engine.AI.custom_tasks import *


class AIEntity:
	"""
	Object that represent a character played by an Artificial Intelligence
	"""
	def __init__(self, character):
		self.character = character
		self.blackboard = {}
		self.behaviour_tree = None
		self.is_behaviour_tree_initialized = False
		self._trajectory_changed = False
		self._is_frame_ended = False
	
	def trajectory_changed(self):
		"""
		Check if ball trajectory has changed

		:return: True if trajectory changed, False else
		:rtype bool:
		"""
		return self._trajectory_changed
	
	def change_trajectory(self):
		"""
		Set :var self._trajectory_changed: to True.

		:return: None
		"""
		self._trajectory_changed = True
	
	def reset_change_trajectory(self):
		"""
		Set :var self._trajectory_changed: to False.

		:return: None
		"""
		self._trajectory_changed = False
	
	def end_frame(self):
		"""
		End current frame and notify that frame was spent.

		Call this method in a Behaviour Tree Leaf if no more actions have to be done in current frame.
		:return: None
		"""
		self._is_frame_ended = True
	
	def is_frame_ended(self):
		"""
		Return True if frame is ended.

		:rtype bool:
		"""
		return self._is_frame_ended
		
	def _create_behaviour_tree_1v1(self):
		"""
		Create Behaviour Tree for 1v1 mode.

		:return: None
		"""

		# run and smash
		smash_sequence = Sequence(self)
		smash_sequence.get_control().add(MoveToSmashingPosition(self))
		smash_sequence.get_control().add(JumpForSmashing(self))
		smash_sequence.get_control().add(RandomSmash(self))
		smash_sequence = SmashSequenceDecorator(self, smash_sequence)

		# random throw or throw after diving
		random_throw_or_dive = Selector(self)
		random_throw_or_dive.get_control().add(ThrowAfterDiving(self))
		random_throw_or_dive.get_control().add(RandomThrow(self))

		# find target ball position, run to it and throw
		catch_ball_sequence = Sequence(self)
		catch_ball_sequence.get_control().add(FindBallTargetPosition(self))
		catch_ball_sequence.get_control().add(MoveToTargetPosition(self))
		catch_ball_sequence.get_control().add(random_throw_or_dive)

		# random throw or smash
		# TODO: add conditions to check before smashing ! Just for test
		smash_or_throw = Selector(self)
		smash_or_throw.get_control().add(smash_sequence)
		smash_or_throw.get_control().add(catch_ball_sequence)
		smash_or_throw = MoveAndThrowDecorator(self, smash_or_throw)

		# wait and serve
		serve = Sequence(self)
		serve.get_control().add(Wait(self, duration=500))
		serve.get_control().add(RandomThrow(self))
		serve = WaitAndServe(self, serve)

		# replace and idling
		replace_and_idling_sequence = Sequence(self)
		replace_and_idling_sequence.get_control().add(ChooseIdlingPosition(self))
		replace_and_idling_sequence.get_control().add(MoveToIdlingPosition(self))
		replace_and_idling_sequence.get_control().add(Idle(self))
		replace_and_idling_sequence = MoveAndIdleDecorator(self, replace_and_idling_sequence)

		# root
		b_tree = Selector(self)
		b_tree.get_control().add(serve)
		b_tree.get_control().add(replace_and_idling_sequence)
		b_tree.get_control().add(smash_or_throw)
		b_tree = ResetDecorator(self, b_tree)
		
		self.behaviour_tree = b_tree

	def create(self):
		self._create_behaviour_tree_1v1()

	def update(self):
		"""
		Update behaviour tree for this AI Entity.

		If not initialized, behaviour tree is started.

		:return: None
		"""
		if not self.is_behaviour_tree_initialized:
			self.is_behaviour_tree_initialized = True
			self.behaviour_tree.start()

		# max iteration to prevent infinite loop (behaviour tree leaves without end_frame() call)
		n_max = 100
		n = 0
		while not self.is_frame_ended() and n < n_max:
			self.behaviour_tree.do_action()
			n += 1
		if n == n_max:
			print("possible infinite loop in ai_entity update")
		self._is_frame_ended = False
