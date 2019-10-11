# encoding : UTF-8

from Engine.AI.behaviour_tree import *
from Engine.Trajectory.thrower_manager import ThrowerManager
from Settings.general_settings import *
from Game.character_states import Serving
from Engine import game_engine


import pygame as pg
from random import randint


def should_ai_move_to_the_ball(ai_entity):
	"""
	Check if specified AI entity should move to the ball to throw it.
	
	:param AIEntity ai_entity: specified AI entity
	:return: True if AI entity should move to target position
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


def move_to(ai_entity, target, thr=0.1):
	"""
	Make AI entity to move to a specified target position.

	:param AI_Entity ai_entity: AI entity who is going to move to target position
	:param pygame.Vector3 target: target position
	:param float thr: threshold for x and y axis which final position is considered as target
	:return: None
	"""
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


def should_ai_serve(ai_entity):
	"""
	Check if specified AI entity should serve.

	:param AIEntity ai_entity: specified AI entity
	:return: True if AI entity has to serve
	:rtype bool:
	"""
	character_state_type = ai_entity.character.state.__class__.type
	if character_state_type == CharacterStateType.SERVING:
		return not ai_entity.character.state.has_served
	return False


def should_ai_dive(ai_entity):
	"""
	Check if specified AI entity has to dive to catch ball instead of running.

	:param AIEntity ai_entity: specified AI entity
	:return:
		(True, delta_xy) if AI entity should dive in :var delta_xy: direction,
		(False, None) else.
	;:rtype : (bool, pygame.Vector3) or (bool, None)
	"""
	thrower_manager = ThrowerManager.get_instance()
	trajectory = thrower_manager.current_trajectory

	if trajectory is not None:
		# TODO: change by comparing time to reach target position, by running or diving.
		# remaining time in ms before ball touches ground (with marge m)
		final_t = int(trajectory.t0 + 1000 * trajectory.get_final_time())
		delta_t = final_t - game_engine.GameEngine.get_instance().get_running_ticks()

		# distance between character and target position
		delta_xy = ai_entity.blackboard["target_position"] - ai_entity.character.position
		delta_xy.z = 0
		dis = delta_xy.length()

		# distance travelled by running or diving, shape of collider taken in account
		run_distance = RUN_SPEED * delta_t / 1000 + CHARACTER_W / 2
		dive_distance = DIVE_SPEED * min(delta_t, DIVE_SLIDE_DURATION) / 1000 + CHARACTER_H - CHARACTER_W / 2

		if run_distance < dis <= dive_distance:
			return True, delta_xy
	return False, None


def dive(ai_entity, dxy):
	"""
	Make AI entity to dive in a direction.

	Given direction is continuous, but not resulting diving direction (8 possible directions)
	:param AIEnity ai_entity: AI entity who's going to dive
	:param pygame.Vector3 dxy: direction of diving
	:return: None
	"""
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
	ai_entity.end_frame()


class MoveAndThrowDecorator(TaskDecorator):
	def do_action(self):
		self.task.do_action()

	def check_conditions(self):
		b_do_action = should_ai_move_to_the_ball(self.ai_entity)
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
		if should_ai_serve(self.ai_entity):
			self.get_control().finish_with_failure()

		if should_ai_move_to_the_ball(self.ai_entity):
			self.get_control().finish_with_failure()

		# move to idling position
		idling_pos = Vector3(CHARACTER_INITIAL_POS)
		if self.ai_entity.character.team.id == TeamId.LEFT:
			idling_pos.y *= -1
		pos_is_reached = move_to(self.ai_entity, idling_pos)

		# if idling position reached --> success
		if pos_is_reached:
			self.get_control().finish_with_success()


class MoveAndIdleDecorator(TaskDecorator):
	def do_action(self):
		self.task.do_action()

	def check_conditions(self):
		b_do_action = not should_ai_move_to_the_ball(self.ai_entity)
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


class ThrowAfterDiving(LeafTask):
	def check_conditions(self):
		return self.ai_entity.character.is_state_type_of(CharacterStateType.DIVING)

	def do_action(self):
		character = self.ai_entity.character

		if character.is_colliding_ball:
			ev = pg.event.Event(ACTION_EVENT, {"player_id": character.player_id, "action": PlayerAction.THROW_BALL})
			pg.event.post(ev)
			# we can set a direction for draft throw here by sending events

			self.get_control().finish_with_success()
		self.ai_entity.end_frame()


class Idle(LeafTask):
	def check_conditions(self):
		b_do_action = not should_ai_move_to_the_ball(self.ai_entity)
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
		