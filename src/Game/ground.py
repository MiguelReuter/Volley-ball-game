# encoding : UTF-8

from Engine.Display.scalable_sprite import ScalableSprite, get_scaled_rect_from
import Engine

from Settings import NOMINAL_RESOLUTION, COURT_DIM_X

from pygame import Vector3
import pygame as pg

from random import randint


X_MAX = COURT_DIM_X / 2 + 5


class Ground(ScalableSprite):
	def __init__(self):
		ScalableSprite.__init__(self)

		# for detecting camera changes and to update ground sprite
		self.prev_camera_position = None
		self.prev_cam_focus_point = None

		self.create()

	def create(self):
		# create a filled rect from 3D x coordinates = -X_MAX
		cam = Engine.Display.display_manager.DisplayManager.get_instance().camera

		# camera properties
		self.prev_camera_position = Vector3(cam.position)
		self.prev_cam_focus_point = Vector3(cam.focus_point)

		# image is still at same size, only changing rect
		raw_image = pg.Surface(NOMINAL_RESOLUTION)

		self.update_raw_rect(cam)
		self.image = raw_image

		self.fill_surface()

	def fill_surface(self):
		palette = Engine.Display.display_manager.DisplayManager.get_instance().palette
		cols = [palette[5], palette[11], palette[14]]
		# cols = [palette[5]]

		w, h = self._raw_image.get_size()
		for y in range(h):
			for x in range(w):
				col = cols[randint(0, len(cols)-1)]
				self._raw_image.set_at((x, y), col)

	def update_raw_rect(self, camera):
		self.dirty = 1

		_, v = camera.world_to_pixel_coords(Vector3(-X_MAX, 0, 0), NOMINAL_RESOLUTION)
		size = (NOMINAL_RESOLUTION[0], NOMINAL_RESOLUTION[1] - v)

		raw_rect = pg.Rect((0, v), size)

		if self._raw_rect is None:
			return_rect = raw_rect
		else:
			# TODO: maybe change this
			x = 0
			y = min(raw_rect.y, self._raw_rect.y)
			w = self._raw_rect.w
			h = abs(raw_rect.y - self._raw_rect.y)
			return_rect = pg.Rect(x, y, w, h)
		self.rect = raw_rect

		return return_rect

	def update(self, *args):
		"""
		Update image if camera properties changed.

		This method is an override of Sprite.update(*args).
		:param args:
		:return: None
		"""
		# update image
		cam = Engine.Display.display_manager.DisplayManager.get_instance().camera
		if cam.position.z != self.prev_camera_position.z or cam.focus_point.z != self.prev_cam_focus_point.z:
			self.prev_camera_position = Vector3(cam.position)
			self.prev_cam_focus_point = Vector3(cam.focus_point)

			r = self.update_raw_rect(cam)
			ScalableSprite.update(self, r)


