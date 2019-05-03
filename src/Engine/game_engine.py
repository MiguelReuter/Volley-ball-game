# encoding : UTF-8

from .Display import *
from .Input import *

from Settings import *
from Game.ball import Ball
from Game.court import Court
from Game.character import Character
from Game.character_states import *

from Engine.Collisions import *
from .TrajectorySolver import ThrowerManager


import pygame as pg


INITIAL_POS = pg.Vector3(-2, 5, 1)
TARGET_POS = pg.Vector3(-2, -3, 0.5)
WANTED_H = 3.5


class GameEngine:
	# TODO : singleton
	def __init__(self):
		self.display_manager = DisplayManager(self)
		self.input_manager = InputManager(self)
		self.collisions_manager = CollisionsManager(self)
		self.thrower_manager = ThrowerManager()
		self.running = True
		self._create()
	
	def _create(self):
		self.ball = Ball(INITIAL_POS, BALL_RADIUS)
		self.court = Court(COURT_DIM_Y, COURT_DIM_X, NET_HEIGHT_BTM, NET_HEIGHT_TOP)
		self.char1 = Character((-2, -3.5, 0))
		self.char2 = Character((0, 5, 0))
		self.objects = [self.court, self.ball, self.char1, self.char2]
		
		# allowed pygame events
		pg.event.set_blocked([i for i in range(pg.NUMEVENTS)])
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT, pg.VIDEORESIZE,
		                      ACTIONEVENT, THROW_EVENT, TRAJECTORY_CHANGED_EVENT])

	def request_quit(self):
		"""
		Call this method to quit main loop and game.
		
		:return: None
		"""
		self.running = False
	
	def serve(self):
		self.char1.position = Vector3(2, -5, 0)
		self.ball.will_be_served = True
		self.ball.position = self.char1.get_hands_position()
		self.char1.state = Serving(self.char1)
	
	def update_actions(self, action_events, dt):
		for event in action_events:
			action = event.action
			if action == "QUIT":
				self.running = False
			elif action == "PAUSE":
				print(action, "not implemented yet")
			elif action == "SPACE_TEST":
				#self.serve()
				self.thrower_manager.throw_ball(self.ball, INITIAL_POS, TARGET_POS, WANTED_H)
				#self.thrower_manager.throw_at_random_target_position(self.ball, INITIAL_POS, WANTED_H)
		
	def run(self):
		"""
		Main loop, call different managers (input, display...) etc.
		
		:return: None
		"""
		frame_count = 0
		
		cam = self.display_manager.camera

		# ball initial velocity
		self.thrower_manager.throw_ball(self.ball, INITIAL_POS, TARGET_POS, WANTED_H)
		
		# for frame rate
		t2 = pg.time.get_ticks()
		t1 = t2
		t0 = t2  # time of first frame of the game
		while self.running:
			# PHYSICS
			self.ball.update_physics(t2-t1)
			for char in [self.char1, self.char2]:
				char.update_physics(t2-t1)
			
			# COLLISIONS
			self.collisions_manager.update(self.ball, self.court, [self.char1, self.char2])
			
			# KB EVENTS
			self.input_manager.update()
			# TODO : take in account origin of action event (player index for ex.) ?
			actions_events_queue = pg.event.get(ACTIONEVENT)
			# UPDATE ACTIONS
			# TODO : iterator for objects who have update_actions method
			self.char1.update_actions(actions_events_queue, t2 - t1)
			cam.update_actions(actions_events_queue, t2 - t1)
			self.update_actions(actions_events_queue, t2 - t1)
			
			# throw event
			self.thrower_manager.update(pg.event.get(THROW_EVENT), pg.event.get(TRAJECTORY_CHANGED_EVENT), self.ball)
			
			# DISPLAY
			self.display_manager.update([*self.objects, self.thrower_manager])

			# manage frame rate
			t1 = t2
			t2 = pg.time.get_ticks()
			pg.time.wait(int(1000 / NOMINAL_FRAME_RATE - (t2 - t1)))
			frame_count += 1

		print("run with {} mean fps".format(int(1000 * frame_count / (t2 - t0))))


		