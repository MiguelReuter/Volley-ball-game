# encoding : UTF-8

from Engine import *
from Engine.Display import *
from Engine.Input import *

from settings import *
from Game.ball import Ball
from Game.court import Court
from Game.character import Character

from Engine.Collisions import *

import pygame as pg


class GameEngine:
	# TODO : singleton
	def __init__(self):
		self.display_manager = DisplayManager(self)
		self.input_manager = InputManager(self)
		self.collisions_manager = CollisionsManager(self)
		self.running = True
		self._create()
	
	def _create(self):
		self.ball = Ball((-2, 1, 3), 0.5)
		self.court = Court(10, 6, 1.5, 3)
		self.char1 = Character((-2, -3.5, 0))
		self.char2 = Character((2, 2, 0))
		self.objects = [self.court, self.ball, self.char1, self.char2]
		
		# allowed pygame events
		pg.event.set_blocked([i for i in range(pg.NUMEVENTS)])
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT, pg.VIDEORESIZE,
		                      ACTIONEVENT, THROWEVENT])

	def request_quit(self):
		"""
		Call this method to quit main loop and game.
		
		:return: None
		"""
		self.running = False
		
	def update_actions(self, action_events, dt):
		for event in action_events:
			action = event.action
			if action == "QUIT":
				self.running = False
			elif action == "PAUSE":
				print(action, "not implemented yet")
			elif action == "SPACE_TEST":
				# debug window resize
				size = (1200, 800)
				resize_event = pg.event.Event(pg.VIDEORESIZE, {"size": size, 'w': size[0], 'h': size[1]})
				pg.event.post(resize_event)
				
				# debug ball position
				print("ball position :", self.ball.position)
	
	def update_ball_throwing(self):
		for ev in pg.event.get(THROWEVENT):
			self.ball.velocity = ev.velocity
		
	def run(self):
		"""
		Main loop, call different manager (input, display...) etc.
		
		:return: None
		"""
		frame_count = 0
		
		cam = self.display_manager.camera

		# ball initial velocity
		self.ball.velocity += (0, -4, 4)

		# for frame rate
		t2 = pg.time.get_ticks()
		t1 = t2
		t0 = t2  # time of first frame of the game
		while self.running:
			# PHYSICS
			self.ball.update_physics(t2-t1)
			
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
			self.update_ball_throwing()
			
			# DISPLAY
			self.display_manager.update(self.objects)

			# manage frame rate
			t1 = t2
			t2 = pg.time.get_ticks()
			pg.time.wait(int(1000 / NOMINAL_FRAME_RATE - (t2 - t1)))
			frame_count += 1

		print("run with {} mean fps".format(int(1000 * frame_count / (t2 - t0))))


		