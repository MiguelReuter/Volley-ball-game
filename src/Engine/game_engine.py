# encoding : UTF-8

from Engine import *
from Engine.Display import *
from Engine.Input import *

from settings import *
from Game.ball import Ball
from Game.court import Court
from Game.character import Character

import pygame as pg
from math import log2, pow

class GameEngine:
	# TODO : singleton
	def __init__(self):
		self.screen = None  # will be set in self._create_window()
		
		self.window_mode = WindowMode.FIXED_SIZE
		self.window_resize_2n = WINDOW_RESIZE_2N
		self.screen_scale_factor_2n = None
		self._create_window()
		
		self.display_manager = DisplayManager(self, debug_surface_size=self.screen.get_size())
		self.input_manager = InputManager(self)

		self.running = True
		self._create()
	
	def _create(self):
		self.ball = Ball((1, 1, 3), 0.5)
		self.court = Court(10, 6, 1.5, 3)
		self.char1 = Character((-2, -2, 0))
		self.char2 = Character((2, 2, 0))
		self.objects = [self.court, self.ball, self.char1, self.char2]
		
	def _create_window(self):
		w, h = NOMINAL_RESOLUTION
		if self.window_mode == WindowMode.FIXED_SIZE:
			if not self.window_resize_2n:
				pass
			else:
				self.screen_scale_factor_2n = self._process_screen_factor_scale()
				w = int(NOMINAL_RESOLUTION[0] * pow(2, self.screen_scale_factor_2n))
				h = int(NOMINAL_RESOLUTION[1] * pow(2, self.screen_scale_factor_2n))
		elif self.window_mode == WindowMode.RESIZABLE:
			# TODO : to implement
			print(self.window_mode, " mode not implemented")
		elif self.window_mode == WindowMode.FULL_SCREEN:
			# TODO : to implement
			print(self.window_mode, " mode not implemented")
		
		self.screen = pg.display.set_mode((w, h))
		self.surface = pg.Surface((w, h))
		pg.display.set_caption(CAPTION_TITLE)
	
	def _resize_surface(self, surface):
		if self.window_mode == WindowMode.FIXED_SIZE and self.window_resize_2n:
			new_size = list(surface.get_size())
			new_surface = pg.Surface(new_size)
			new_surface.blit(surface, (0, 0))
			for _ in range(self.screen_scale_factor_2n):
				new_size = [new_size[i] * 2 for i in (0, 1)]
				new_surface = pg.transform.scale2x(new_surface)
			return new_surface
		return surface

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
			
			# DISPLAY
			self.display_manager.update(self.objects)
			
			# TODO : move this in DisplayManager + display_manager.surface_wo_scale and display_manager.scaled_surface
			new_surface = self._resize_surface(self.display_manager.surface)
			self.surface.blit(new_surface, (0, 0))
			
			self.screen.blit(self.surface, (0, 0))
			self.screen.blit(self.display_manager.debug_surface, (0, 0))

			# update screen
			pg.display.flip()

			# KB EVENTS
			self.input_manager.update()
			
			# TODO : take in account origin of action event (player index for ex.) ?
			actions_events_queue = pg.event.get(ACTIONEVENT)
			# UPDATE ACTIONS
			self.char1.update_actions(actions_events_queue, t2 - t1)
			cam.update_actions(actions_events_queue, t2 - t1)
			self.update_actions(actions_events_queue, t2 - t1)

			# manage frame rate
			t1 = t2
			t2 = pg.time.get_ticks()
			pg.time.wait(int(1000 / NOMINAL_FRAME_RATE - (t2 - t1)))
			frame_count += 1

		print("run with {} mean fps".format(int(1000 * frame_count / (t2 - t0))))

	def _process_screen_factor_scale(self):
		f_w = int(log2(pg.display.Info().current_w / NOMINAL_RESOLUTION[0]))
		f_h = int(log2(pg.display.Info().current_h / NOMINAL_RESOLUTION[1]))
		return min(f_w, f_h)
		