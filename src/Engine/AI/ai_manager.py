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

	def add_entity(self, character):
		"""
		Add an AI Entity, to link to a specific character.

		:param Game.Character character: character to assign to new AIEntity
		:return: None
		"""
		new_entity = AIEntity(character)
		new_entity.create()

		self.entities += [new_entity]

	def reset(self):
		self.entities = []

	def update(self):
		"""
		Update all AI Entities.

		:return: None
		"""
		# check if trajectory changed
		if ThrowerManager.get_instance().trajectory_changed:
			ThrowerManager.get_instance().trajectory_changed = False
			for entity in self.entities:
				entity.change_trajectory()
				
		# update
		for entity in self.entities:
			entity.update()
