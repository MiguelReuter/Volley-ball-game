# encoding : UTF-8

import pygame as pg

from Settings.general_settings import BKGND_TRANSPARENCY_COLOR, NOMINAL_RESOLUTION


class Scene3D(pg.sprite.LayeredDirty):
	def __init__(self):
		pg.sprite.LayeredDirty.__init__(self)
		self.image = None

		self.rect_list = []

	def create(self):
		# create sprites and add them
		# self.add(sp)

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

		# court ground

		# shadows

		# characters and ball if opposite camera side (along y axis)

		# net

		# characters and ball if same camera side
