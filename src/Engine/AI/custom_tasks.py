# encoding : UTF-8

from Engine.AI.behaviour_tree import *
from Engine.Trajectory.thrower_manager import ThrowerManager
from Settings.general_settings import *

import pygame as pg
from random import randint


def should_i_run_to_the_ball(ai_entity):
	"""
	Check if specified AI entity should run to the ball to throw it.
	
	:param AIEntity ai_entity: specified AI entity
	:return: True if AI entity should run
	:rtype bool:
	"""
	character = ai_entity.blackboard["character"]
	
	thrower_manager = ThrowerManager.get_instance()
	
	if thrower_manager.current_trajectory.target_pos is not None:
		target_pos = Vector3(thrower_manager.current_trajectory.target_pos)
		# if ball will not reached same court side than character
		if (target_pos.y > 0 and character.is_in_left_side) or (target_pos.y < 0 and not character.is_in_left_side):
			return False
		
		# TODO: implement other checks (game rules): if pass number < MAX_PASS_NUMBER...
		
		return True
	return False


class MoveAndThrowDecorator(TaskDecorator):
	def do_action(self):
		self.task.do_action()

	def check_conditions(self):
		return should_i_run_to_the_ball(self._blackboard["ai_entity"])
	

class FindBallTargetPosition(LeafTask):
	def do_action(self):
		"""
		Find target ball position and write it in blackboard.

		:return: None
		"""
		print("find ball target position")
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
		
		if (target_pos.y > 0 and character.is_in_left_side) or (target_pos.y < 0 and not character.is_in_left_side):
			print("not for me !")
			self.get_control().finish_with_failure()
		else:
			print("for me")
			self.get_control().finish_with_success()


class MoveToTargetPosition(LeafTask):
	def start(self):
		print("i'm moving")

	def do_action(self):
		target_pos = self._blackboard["target_position"]
		character = self._blackboard["character"]
		ai_entity = self._blackboard["ai_entity"]
		
		dxy = target_pos - character.position
		thr = 0.1
		events_map = {"MOVE_UP": dxy[0] < -thr, "MOVE_DOWN": dxy[0] > thr,
		              "MOVE_RIGHT": dxy[1] > thr, "MOVE_LEFT": dxy[1] < -thr}
		for action in events_map.keys():
			if events_map[action]:
				ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": action})
				pg.event.post(ev)

		self._blackboard["frame_consumed"] = True
		
		# if position reached
		if abs(dxy[0]) < thr and abs(dxy[1]) < thr:
			print("position reached")
			self.get_control().finish_with_success()
			
		if ai_entity.get_and_reset_flag_value("trajectory_changed"):
			print("trajectory changed [moving]")
			self.get_control().finish_with_failure()  # TODO: change, need to reset and run sequence again instead
			
		if character.is_colliding_ball:
			self.get_control().finish_with_success()


class RandomThrow(LeafTask):
	def start(self):
		print("i'm throwing !")
	
	def do_action(self):
		ai_entity = self._blackboard["ai_entity"]
		character = self._blackboard["character"]
		self._blackboard["frame_consumed"] = True
		
		if ai_entity.get_and_reset_flag_value("trajectory_changed"):
			self.get_control().finish_with_failure()

		if character.is_colliding_ball:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": "THROW_BALL"})
			pg.event.post(ev)

			# random direction
			left_right_action = ("MOVE_LEFT", "MOVE_RIGHT", None)[randint(0, 2)]
			up_down_action = ("MOVE_UP", "MOVE_DOWN", None)[randint(0, 2)]
			for action in (left_right_action, up_down_action):
				if action is not None:
					ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": action})
					pg.event.post(ev)
			
			self.get_control().finish_with_success()


class IdleUntilTrajectoryChanged(LeafTask):
	def check_conditions(self):
		return not should_i_run_to_the_ball(self._blackboard["ai_entity"])
	
	def start(self):
		print("idling...")

	def do_action(self):
		print("...")
		ai_entity = self._blackboard["ai_entity"]

		if ai_entity.get_and_reset_flag_value("trajectory_changed"):
			print("trajectory changed [idling]")
			self.get_control().finish_with_success()
		self._blackboard["frame_consumed"] = True

