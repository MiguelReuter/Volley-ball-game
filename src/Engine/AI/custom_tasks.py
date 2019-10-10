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


def should_ai_dive(ai_entity):
	thrower_manager = ThrowerManager.get_instance()
	trajectory = thrower_manager.current_trajectory

	if trajectory is not None:
		# remaining time in ms before ball touches ground (with marge m)
		m = 0.2
		final_t = int(trajectory.t0 + 1000 * trajectory.get_time_at_z(BALL_RADIUS + m))
		delta_t = final_t - game_engine.GameEngine.get_instance().get_running_ticks()

		# distance between character and target position
		# TODO: add trajectory.get_pos_at_t(ti) instead of target_position (not really target_position with marge m)
		delta_xy = ai_entity.blackboard["target_position"] - ai_entity.character.position
		delta_xy.z = 0
		dis = delta_xy.length()

		# distance travelled by running or diving, shape of collider taken in account
		run_distance = RUN_SPEED * delta_t / 1000 + CHARACTER_W / 2
		dive_distance = DIVE_SPEED * min(delta_t, DIVE_SLIDE_DURATION) / 1000 + CHARACTER_H - CHARACTER_W / 2

		# print("run: ", run_distance, "dive: ", dive_distance, "distance: ", d)
		if run_distance < dis <= dive_distance:
			return True, delta_xy
	return False, None


def dive(ai_entity, dxy):
	# dive action event will be posted
	dive_actions = [PlayerAction.DIVE]

	if dxy.x < -CHARACTER_W / 2:
		dive_actions.append(PlayerAction.MOVE_UP)
	elif dxy.x > CHARACTER_W / 2:
		dive_actions.append(PlayerAction.MOVE_DOWN)
	if dxy.y < -CHARACTER_W / 2:
		dive_actions.append(PlayerAction.MOVE_LEFT)
	elif dxy.y > CHARACTER_W / 2:
		dive_actions.append(PlayerAction.MOVE_RIGHT)

	for act in dive_actions:
		ev = pg.event.Event(ACTION_EVENT, {"player_id": ai_entity.character.player_id, "action": act})
		pg.event.post(ev)


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


def move_to(ai_entity, target, thr=0.1):
	character = ai_entity.character

	dxy = target - character.position
	events_map = {PlayerAction.MOVE_UP: dxy[0] < -thr, PlayerAction.MOVE_DOWN: dxy[0] > thr,
				  PlayerAction.MOVE_RIGHT: dxy[1] > thr, PlayerAction.MOVE_LEFT: dxy[1] < -thr}
	for action in events_map.keys():
		if events_map[action]:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": action})
			pg.event.post(ev)

	ai_entity.end_frame()

	# if position reached
	return abs(dxy[0]) < thr and abs(dxy[1]) < thr


class MoveToTargetPosition(LeafTask):
	def start(self):
		pass

	def do_action(self):
		b_dive, delta_xy = should_ai_dive(self.ai_entity)
		if b_dive:
			dive(self.ai_entity, delta_xy)
			self.get_control().finish_with_success()
		else:
			pos_is_reached = move_to(self.ai_entity, self.ai_entity.blackboard["target_position"])

			if pos_is_reached:
				self.get_control().finish_with_success()

			if self.ai_entity.trajectory_changed():
				self.ai_entity.reset_change_trajectory()
				self.get_control().finish_with_failure()

			if self.ai_entity.character.is_colliding_ball:
				self.get_control().finish_with_success()


class MoveToIdlingPosition(LeafTask):
	def do_action(self):
		idling_pos = Vector3(CHARACTER_INITIAL_POS)
		if self.ai_entity.character.team.id == TeamId.LEFT:
			idling_pos.y *= -1

		pos_is_reached = move_to(self.ai_entity, idling_pos)
		if pos_is_reached:
			self.get_control().finish_with_success()

		if should_ai_run_to_the_ball(self.ai_entity):
			self.get_control().finish_with_failure()


class MoveAndIdleDecorator(TaskDecorator):
	def do_action(self):
		self.task.do_action()

	def check_conditions(self):
		b_do_action = not should_ai_run_to_the_ball(self.ai_entity)
		b_do_action &= not should_ai_serve(self.ai_entity)
		return b_do_action


class RandomThrow(LeafTask):
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
		