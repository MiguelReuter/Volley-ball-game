# encoding : UTF-8

import pygame as pg
from settings import *


class InputManager:
	# TODO : singleton
	def __init__(self, game_engine):
		self.game_engine = game_engine
		self.keys = {k: KeyState.RELEASED for k in KEYS}
		
	def update(self):
		# update state
		for k in self.keys:
			if self.keys[k] == KeyState.JUST_PRESSED:
				self.keys[k] = KeyState.PRESSED
			elif self.keys[k] == KeyState.JUST_RELEASED:
				self.keys[k] = KeyState.RELEASED
				
		# detect a state modification (with pygame event)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.game_engine.request_quit()
			if event.type == pg.KEYDOWN:
				if event.key in KEYS:
					self.keys[event.key] = KeyState.JUST_PRESSED

			if event.type == pg.KEYUP:
				if event.key in KEYS:
					self.keys[event.key] = KeyState.JUST_RELEASED