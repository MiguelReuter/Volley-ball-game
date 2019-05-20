# encoding : UTF-8

import Engine.game_engine
from Settings.general_settings import *
from Engine.AI.AI_instance import AIInstance


class AIManager:
	s_instance = None

	@staticmethod
	def get_instance():
		return AIManager.s_instance

	def __init__(self):
		AIManager.s_instance = self
		self.ia_instances = []

	def create(self):
		game_engine = Engine.game_engine.GameEngine.get_instance()

		# characters which need an AI
		self.ia_instances = [AIInstance(c) for c in game_engine.characters
							 if c.player_id.value <= PlayerId.IA_ID_1.value]

	def update(self):
		for ia_instance in self.ia_instances:
			ia_instance.update()
