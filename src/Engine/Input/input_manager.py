# encoding : UTF-8

import pygame as pg
from settings import *


class InputManager:
	def __init__(self, game_engine):
		self.game_engine = game_engine
		self.keys = {k: KeyState.UNPRESSED for k in KEYS}
		
	def update(self):
		# update state
		for k in self.keys:
			if self.keys[k] == KeyState.JUST_PRESSED:
				self.keys[k] = KeyState.PRESSED
			elif self.keys[k] == KeyState.JUST_RELEASE:
				self.keys[k] = KeyState.UNPRESSED
				
		# detect a state modification (with pygame event)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.game_engine.request_quit()
			if event.type == pg.KEYDOWN:
				if event.key in KEYS:
					self.keys[event.key] = KeyState.JUST_PRESSED

			if event.type == pg.KEYUP:
				if event.key in KEYS:
					self.keys[event.key] = KeyState.JUST_RELEASE