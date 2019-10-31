# encoding : UTF-8

import pygame as pg

from Settings.general_settings import BKGND_TRANSPARENCY_COLOR, NOMINAL_RESOLUTION

from Game.ground import Ground


class Scene3D(pg.sprite.LayeredDirty):
	def __init__(self):
		pg.sprite.LayeredDirty.__init__(self)
		self.image = None

		# sprites
		self.ground = None
		self.ball = None

		self.rect_list = []

		self.create()

	def create(self):
		# create sprites and add them
		self.ground = Ground()
		self.add(self.ground)

		# create image
		self.create_image(NOMINAL_RESOLUTION)

	def create_image(self, size=(0, 0)):
		"""
		Create image and set colorkey.

		:param tuple(int, int) size: size of image to create
		:return: None
		"""
		self.image = pg.Surface(size)
		self.image.fill(BKGND_TRANSPARENCY_COLOR)
		self.image.set_colorkey(BKGND_TRANSPARENCY_COLOR)

	def update(self):
		"""
		Update image and list of rects to redraw.

		For each frame, sprites that need to be redraw are cleared and draw.

		:return: None
		"""
		pg.sprite.LayeredDirty.update(self)

		# ground
		if self.ground.dirty > 0:
			for r in self.ground.rect_list_to_redraw:
				self.image.fill(BKGND_TRANSPARENCY_COLOR, r)
		else:
			if self.ground.source_rect is not None:
				self.image.fill(BKGND_TRANSPARENCY_COLOR, self.ground.source_rect)
		# court lines

		# shadows

		# characters and ball if opposite camera side (along y axis)
		if self.ball is not None:
			if self.ball.dirty > 0:
				for r in self.ball.rect_list_to_redraw:
					self.image.fill(BKGND_TRANSPARENCY_COLOR, r)
			else:
				if self.ball.source_rect is not None:
					self.image.fill(BKGND_TRANSPARENCY_COLOR, self.ball.source_rect)

		# net

		# characters and ball if same camera side

		self.rect_list = pg.sprite.LayeredDirty.draw(self, self.image)

	def set_ball_sprite(self, ball):
		# remove old ball sprite
		self.remove(self.ball)

		# set new ball sprite
		self.ball = ball
		self.add(self.ball)
