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
		
	def get_and_reset_flag_value(self, flag):
		if flag in self.blackboard.keys():
			if self.blackboard[flag]:
				self.blackboard[flag] = False
				return True
			return False
	
	def trajectory_changed(self):
		return self._trajectory_changed
	
	def change_trajectory(self):
		self._trajectory_changed = True
	
	def reset_change_trajectory(self):
		self._trajectory_changed = False
	
	def end_frame(self):
		self._is_frame_ended = True
	
	def is_frame_ended(self):
		return self._is_frame_ended
		
	def _create_behaviour_tree_1v1(self):
		"""
		Create Behaviour Tree for 1v1 mode.

		:return: None
		"""
		find_and_run_to_ball_position = Sequence(self)

		# find target ball position and run to it
		find_and_run_to_ball_position.get_control().add(FindBallTargetPosition(self))
		find_and_run_to_ball_position.get_control().add(MoveToTargetPosition(self))
		find_and_run_to_ball_position.get_control().add(RandomThrow(self))
		find_and_run_to_ball_position = MoveAndThrowDecorator(self, find_and_run_to_ball_position)
		
		# wait and serve
		wait_and_serve = Sequence(self)
		wait_and_serve.get_control().add(Wait(self, duration=1000))
		wait_and_serve.get_control().add(RandomThrow(self))
		wait_and_serve = WaitAndServe(self, wait_and_serve)
		
		# root
		b_tree = Selector(self)
		b_tree.get_control().add(find_and_run_to_ball_position)
		b_tree.get_control().add(wait_and_serve)
		b_tree.get_control().add(IdleUntilTrajectoryChanged(self))
		b_tree = ResetDecorator(self, b_tree)
		
		
		self.behaviour_tree = b_tree

	def create(self):
		self._create_behaviour_tree_1v1()

	def update(self):
		if not self.is_behaviour_tree_initialized:
			self.is_behaviour_tree_initialized = True
			self.behaviour_tree.start()

		n_max = 100
		n = 0
		while not self.is_frame_ended() and n < n_max:
			self.behaviour_tree.do_action()
			n += 1
		self._is_frame_ended = False
