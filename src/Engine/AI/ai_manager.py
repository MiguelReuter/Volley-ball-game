# encoding : UTF-8

from Engine.AI.ai_entity import AIEntity
from Engine.Trajectory.thrower_manager import ThrowerManager


class AIManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return AIManager.s_instance

	def __init__(self):
		AIManager.s_instance = self

		self.entities = []
		self.blackboard = {}  # common blackboard

	def add_entity(self, character):
		new_entity = AIEntity(character)
		new_entity.create()

		self.entities += [new_entity]

	def update(self):
		# check if trajectory changed
		print("-------------")
		if ThrowerManager.get_instance().trajectory_changed:
			ThrowerManager.get_instance().trajectory_changed = False
			for entity in self.entities:
				entity.blackboard["trajectory_changed"] = True
				
		# update
		for entity in self.entities:
			entity.update()
