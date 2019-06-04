# encoding : UTF-8

from Engine.AI.behaviour_tree import *
from Engine.Trajectory.thrower_manager import ThrowerManager
from Settings.general_settings import *
import pygame as pg


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
			self.get_control().finish_with_failure()
			print("not for me !")
		else:
			print("for me")
			self.get_control().finish_with_success()


class MoveToTargetPosition(LeafTask):
	def do_action(self):
		target_pos = self._blackboard["target_position"]
		character = self._blackboard["character"]

		dxy = target_pos - character.position

		thr = 0.1
		
		events_map = {"MOVE_UP": dxy[0] < -thr, "MOVE_DOWN": dxy[0] > thr,
		              "MOVE_RIGHT": dxy[1] > thr, "MOVE_LEFT": dxy[1] < -thr}
		for action in events_map.keys():
			if events_map[action]:
				ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": action})
				pg.event.post(ev)

		self._blackboard["frame_consumed"] = True

		if abs(dxy[0]) < thr and abs(dxy[1]) < thr:
			# if position reached
			self.get_control().finish_with_success()
			
		if ThrowerManager.get_instance().trajectory_changed:
			self.get_control().finish_with_failure()
		'''
		if character.is_colliding_ball:
			# or if touch ball ?
			self.get_control().finish_with_success()
		# or trajectory changed
		'''


class IdleUntilTrajectoryChanged(LeafTask):
	def do_action(self):
		print("Still waiting")
		if ThrowerManager.get_instance().trajectory_changed:
			print("trajectory changed !")
			self.get_control().finish_with_success()
		self._blackboard["frame_consumed"] = True

