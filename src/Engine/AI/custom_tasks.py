# encoding : UTF-8

from Engine.AI.behaviour_tree import *
from Engine.Trajectory.thrower_manager import ThrowerManager
from Settings.general_settings import *
from Game.character_states import Serving
from Engine import game_engine


import pygame as pg
from random import randint


def should_ai_run_to_the_ball(ai_entity):
	"""
	Check if specified AI entity should run to the ball to throw it.
	
	:param AIEntity ai_entity: specified AI entity
	:return: True if AI entity should run
	:rtype bool:
	"""
	character = ai_entity.character
	
	thrower_manager = ThrowerManager.get_instance()
	current_trajectory = thrower_manager.current_trajectory

	if current_trajectory is not None and current_trajectory.target_pos is not None:
		target_pos = Vector3(current_trajectory.target_pos)
		# if ball will not reached same court side than character
		if (target_pos.y > 0 and character.team.id == TeamId.LEFT) or (target_pos.y < 0 and character.team.id == TeamId.RIGHT):
			return False
		# TODO: implement other checks (game rules): if pass number < MAX_PASS_NUMBER...
		return True
	return False


def should_ai_serve(ai_entity):
	character_state = ai_entity.character.state
	if isinstance(character_state, Serving):
		return not character_state.has_served
	return False


class MoveAndThrowDecorator(TaskDecorator):
	def do_action(self):
		self.task.do_action()

	def check_conditions(self):
		b_do_action = should_ai_run_to_the_ball(self.ai_entity)
		b_do_action &= not should_ai_serve(self.ai_entity)
		return b_do_action
	

class FindBallTargetPosition(LeafTask):
	def do_action(self):
		"""
		Find target ball position and write it in blackboard.

		:return: None
		"""
		# print("find ball target position")
		thrower_manager = ThrowerManager.get_instance()

		target_pos = Vector3(thrower_manager.current_trajectory.target_pos)
		self.ai_entity.blackboard["target_position"] = target_pos

		if target_pos is None:
			self.get_control().finish_with_failure()
		else:
			self.get_control().finish_with_success()


class MoveToTargetPosition(LeafTask):
	def start(self):
		# print("i'm moving")
		pass

	def do_action(self):
		ai_entity = self.ai_entity
		character = ai_entity.character
		target_pos = ai_entity.blackboard["target_position"]
		
		dxy = target_pos - character.position
		thr = 0.1
		events_map = {PlayerAction.MOVE_UP: dxy[0] < -thr, PlayerAction.MOVE_DOWN: dxy[0] > thr,
		              PlayerAction.MOVE_RIGHT: dxy[1] > thr, PlayerAction.MOVE_LEFT: dxy[1] < -thr}
		for action in events_map.keys():
			if events_map[action]:
				ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": action})
				pg.event.post(ev)

		self.ai_entity.end_frame()
		
		# if position reached
		if abs(dxy[0]) < thr and abs(dxy[1]) < thr:
			# print("position reached")
			self.get_control().finish_with_success()
			
		if ai_entity.trajectory_changed():
			ai_entity.reset_change_trajectory()
			# print("trajectory changed [moving]")
			self.get_control().finish_with_failure()
			
		if character.is_colliding_ball:
			self.get_control().finish_with_success()


class RandomThrow(LeafTask):
	def start(self):
		# print("i'm throwing !")
		pass
	
	def do_action(self):
		ai_entity = self.ai_entity
		character = ai_entity.character
		ai_entity.end_frame()
		
		if ai_entity.trajectory_changed():
			ai_entity.reset_change_trajectory()
			self.get_control().finish_with_failure()

		if character.is_colliding_ball:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": PlayerAction.THROW_BALL})
			pg.event.post(ev)

			# random direction
			left_right_action = (PlayerAction.MOVE_LEFT, PlayerAction.MOVE_RIGHT, None)[randint(0, 2)]
			up_down_action = (PlayerAction.MOVE_UP, PlayerAction.MOVE_DOWN, None)[randint(0, 2)]
			for action in (left_right_action, up_down_action):
				if action is not None:
					ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": action})
					pg.event.post(ev)
			
			self.get_control().finish_with_success()


class Idle(LeafTask):
	def check_conditions(self):
		b_do_action = not should_ai_run_to_the_ball(self.ai_entity)
		b_do_action &= not should_ai_serve(self.ai_entity)
		
		return b_do_action
	
	def do_action(self):
		# print("idling")
		ai_entity = self.ai_entity

		if ai_entity.trajectory_changed():
			ai_entity.reset_change_trajectory()
			self.get_control().finish_with_success()
			
		if should_ai_serve(ai_entity):
			ai_entity.reset_change_trajectory()
			self.get_control().finish_with_success()
		
		ai_entity.end_frame()


class WaitAndServe(TaskDecorator):
	def do_action(self):
		self.task.do_action()

	def check_conditions(self):
		return should_ai_serve(self.ai_entity)
	
	
class Wait(LeafTask):
	def __init__(self, ai_entity, duration):
		LeafTask.__init__(self, ai_entity)
		self.duration = duration
		self.t0 = None

	def start(self):
		self.t0 = game_engine.GameEngine.get_instance().get_running_ticks()
	
	def do_action(self):
		if game_engine.GameEngine.get_instance().get_running_ticks() - self.t0 > self.duration:
			self.get_control().finish_with_success()
		
		self.ai_entity.end_frame()
		