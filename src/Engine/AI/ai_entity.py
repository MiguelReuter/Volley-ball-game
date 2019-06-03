# encoding : UTF-8

from Engine.AI.custom_tasks import *


class AIEntity:
	def __init__(self, character):
		self.character = character

		self.blackboard = {"character": character,
						   "frame_consumed": False}
		self.behaviour_tree = None

	def _create_behaviour_tree_1v1(self):
		"""
		Create Behaviour Tree for 1v1 mode.

		:return: None
		"""
		bb = self.blackboard
		b_tree = Sequence(bb)

		# find target ball position and run to it
		b_tree.get_control().add(FindBallTargetPosition(bb))
		b_tree.get_control().add(ShouldIRunToTheBall(bb))
		b_tree.get_control().add(MoveToTargetPosition(bb))

		b_tree = ResetDecorator(bb, b_tree)
		self.behaviour_tree = b_tree

	def create(self):
		self._create_behaviour_tree_1v1()
		self.behaviour_tree.start()

	def update(self):
		n_max = 100
		n = 0
		while not self.blackboard["frame_consumed"] and n < n_max:
			self.behaviour_tree.do_action()
			n += 1
		self.blackboard["frame_consumed"] = False
