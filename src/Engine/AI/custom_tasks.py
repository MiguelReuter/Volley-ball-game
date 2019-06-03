# encoding : UTF-8

from Engine.AI.behaviour_tree import *
from Engine.Trajectory.thrower_manager import ThrowerManager
from Engine import game_engine


class FindBallTargetPosition(LeafTask):
	def do_action(self):
		"""
		Find target ball position and write it in blackboard.

		:return: None
		"""
		thrower_manager = ThrowerManager.get_instance()

		target_pos = Vector3(thrower_manager.current_trajectory.target_pos)
		self._blackboard["target_position"] = target_pos

		if target_pos is None:
			self.get_control().finish_with_failure()
		else:
			self.get_control().finish_with_success()


class ShouldIRunToTheBall(LeafTask):
	def do_action(self):
		"""
		:return: None
		"""

		target_pos = self._blackboard["target_position"]
		character = self._blackboard["character"]

		if target_pos.y * character.position.y < 0:
			# TODO : manage finish_with_failure
			# self.get_control().finish_with_failure()
			print("not for me !")
		else:
			print("for me")

		self.get_control().finish_with_success()


class MoveToTargetPosition(LeafTask):
	def __init__(self, blackboard):
		LeafTask.__init__(self, blackboard)

	def do_action(self):
		target_pos = self._blackboard["target_position"]
		character = self._blackboard["character"]

		ge = game_engine.GameEngine.get_instance()

		dxy = target_pos - character.position
		direction = Vector3()

		thr = 0.1
		for i in (0, 1):
			if dxy[i] < -thr:
				direction[i] = -1
			elif dxy[i] > thr:
				direction[i] = 1

		if abs(direction.x) + abs(direction.y) >= 2:
			direction *= 0.7172

		character.move(direction, ge.dt)

		self._blackboard["frame_consumed"] = True

		if direction == Vector3(0, 0, 0):
			# if position reached
			self.get_control().finish_with_success()

		'''
		if character.is_colliding_ball:
			# or if touch ball ?
			self.get_control().finish_with_success()
		# or trajectory changed
		'''



