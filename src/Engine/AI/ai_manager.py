# encoding : UTF-8

from Engine.AI.behaviour_tree import *


class AIManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return AIManager.s_instance

	def __init__(self):
		AIManager.s_instance = self
		
		self.entities = []
		self.blackboard = {}  # TODO : a blackboard for each AI entity + common blackboard (common blackboard
		# reference in blackboard)
		
		self.create_behaviour_tree_1v1()
		
	def create_behaviour_tree_1v1(self):
		"""
		Create Behaviour Tree for 1v1 mode.
		
		:return: None
		"""
		root = Sequence(self.blackboard)
		root = ResetDecorator(self.blackboard, root)
		root.add_task()
		