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
		self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		pg.display.set_caption(CAPTION_TITLE)
		
		self.ball = Ball((1, 1, 3), 0.5)
		self.court = Court(10, 6, 1.5, 3)
		self.char1 = Character((-2, -2, 0))
		self.char2 = Character((2, 2, 0))
		self.objects = [self.court, self.ball, self.char1, self.char2]

	def request_quit(self):
		self.running = False

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
			
			# DISPLAY
			self.display_manager.update(self.objects)
			self.screen.blit(cam.surface, (0, 0))
			# update screen
			pg.display.flip()

			# KB EVENTS
			self.input_manager.update()
			# quit
			if self.input_manager.keys[pg.K_ESCAPE] == KeyState.PRESSED:
				self.running = False
			# move camera
			if self.input_manager.keys[pg.K_UP] == KeyState.PRESSED:
				cam.position += (0, 0, 0.1)
			if self.input_manager.keys[pg.K_DOWN] == KeyState.PRESSED:
				cam.position += (0, 0, -0.1)
			if self.input_manager.keys[pg.K_LEFT] == KeyState.PRESSED:
				cam.position += (0, -0.1, 0)
			if self.input_manager.keys[pg.K_RIGHT] == KeyState.PRESSED:
				cam.position += (0, 0.1, 0)
				
			# move left player
			b_up = self.input_manager.keys[pg.K_z] == KeyState.PRESSED
			b_down = self.input_manager.keys[pg.K_s] == KeyState.PRESSED
			b_left = self.input_manager.keys[pg.K_q] == KeyState.PRESSED
			b_right = self.input_manager.keys[pg.K_d] == KeyState.PRESSED
			self.char1.move(b_up, b_down, b_left, b_right, t2 - t1)

			# debug ball position
			if self.input_manager.keys[pg.K_SPACE] == KeyState.JUST_PRESSED:
				print("ball position :", self.ball.position)

			# manage frame rate
			t1 = t2
			t2 = pg.time.get_ticks()
			pg.time.wait(int(1000 / NOMINAL_FRAME_RATE - (t2 - t1)))
			frame_count += 1

		print("run with {} mean fps".format(int(1000 * frame_count / (t2 - t0))))
