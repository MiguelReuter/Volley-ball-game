# encoding : UTF-8

from Engine.AI.ai_entity import AIEntity


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
		for entity in self.entities:
			entity.update()
