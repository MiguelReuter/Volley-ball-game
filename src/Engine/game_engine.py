# encoding : UTF-8

from Engine import *
from Engine.Display import *
from settings import *
from Game.ball import Ball
from Game.court import Court

import pygame as pg
	
class GameEngine:
	# TODO : singleton
	def __init__(self):
		self.display_manager = DisplayManager(self)
		self._create()
		
		self.ball_pos = pg.Vector3(0, 0, 2)
	
	def _create(self):
		self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		pg.display.set_caption(CAPTION)
		
		self.ball = Ball((1, 1, 3), 0.5)
		self.court = Court(10, 6, 1.5, 3)
		self.objects = [self.court, self.ball]
	
	def run(self):
		running = True
		frame_count = 0

		# ball initial velocity
		self.ball.velocity += (0, -2, 5)

		# for framerate
		t2 = pg.time.get_ticks()
		t1 = t2
		t0 = t2  # time of first frame of the game

		while running:
			##########   PHYSICS   ##########
			self.ball.update_physics(t2-t1)
			
			cam = self.display_manager.camera
			##########   DISPLAY   ##########
			self.display_manager.update(self.objects)
			self.screen.blit(cam.surface, (0, 0))
			# update screen
			pg.display.flip()

			##########   KB EVENTS   ##########
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				if event.type == pg.KEYDOWN:
					# move camera
					if event.key == pg.K_UP:
						cam.position += (0, 0, 0.1)
					if event.key == pg.K_DOWN:
						cam.position += (0, 0, -0.1)
					if event.key == pg.K_LEFT:
						cam.position += (0, -0.1, 0)
					if event.key == pg.K_RIGHT:
						cam.position += (0, 0.1, 0)
					# quit
					if event.key in (pg.K_q, pg.K_ESCAPE):
						running = False
				
				if event.type == pg.KEYUP:
					# debug
					if event.key == pg.K_SPACE:
						print("physics ball pos :", self.ball.position)

			# manage frame rate
			t1 = t2
			t2 = pg.time.get_ticks()
			pg.time.wait(int(1000/NOMINAL_FRAME_RATE - (t2 - t1)))
			frame_count += 1

		print("run with {} mean fps".format(int(1000 * frame_count / (t2 - t0))))
