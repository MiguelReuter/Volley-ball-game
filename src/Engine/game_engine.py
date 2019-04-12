# encoding : UTF-8

from Engine import *
from Engine.Display import *
from Engine.Input import *

from settings import *
from Game.ball import Ball
from Game.court import Court
from Game.character import Character

import pygame as pg


class GameEngine:
	# TODO : singleton
	def __init__(self):
		self.display_manager = DisplayManager(self)
		self.input_manager = InputManager(self)

		self.running = True
		self._create()
	
	def _create(self):
		self.ball = Ball((1, 1, 3), 0.5)
		self.court = Court(10, 6, 1.5, 3)
		self.char1 = Character((-2, -2, 0))
		self.char2 = Character((2, 2, 0))
		self.objects = [self.court, self.ball, self.char1, self.char2]

		pg.event.set_blocked([i for i in range(pg.NUMEVENTS)])
		pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT, pg.VIDEORESIZE, ACTIONEVENT])

	def request_quit(self):
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
	
	def run(self):
		frame_count = 0
		
		cam = self.display_manager.camera

		# ball initial velocity
		self.ball.velocity += (0, -2, 5)

		# for frame rate
		t2 = pg.time.get_ticks()
		t1 = t2
		t0 = t2  # time of first frame of the game

		while self.running:
			# PHYSICS
			self.ball.update_physics(t2-t1)
			
			# KB EVENTS
			self.input_manager.update()
			# TODO : take in account origin of action event (player index for ex.) ?
			actions_events_queue = pg.event.get(ACTIONEVENT)
			# UPDATE ACTIONS
			self.char1.update_actions(actions_events_queue, t2 - t1)
			cam.update_actions(actions_events_queue, t2 - t1)
			self.update_actions(actions_events_queue, t2 - t1)
			
			# DISPLAY
			self.display_manager.update(self.objects)

			# manage frame rate
			t1 = t2
			t2 = pg.time.get_ticks()
			pg.time.wait(int(1000 / NOMINAL_FRAME_RATE - (t2 - t1)))
			frame_count += 1

		print("run with {} mean fps".format(int(1000 * frame_count / (t2 - t0))))


		