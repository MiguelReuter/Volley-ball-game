# encoding : UTF-8

from Engine.Display.scalable_sprite import ScalableSprite, get_scaled_rect_from
import Engine

from Settings import NOMINAL_RESOLUTION, COURT_DIM_X

from pygame import Vector3
import pygame as pg


X_MAX = COURT_DIM_X / 2 + 5


class Ground(ScalableSprite):
	def __init__(self):
		ScalableSprite.__init__(self, 1.0)

		self.rect = None
		self.image = None

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
		raw_image.fill((255, 255, 0))

		self.update_raw_rect(cam)
		self.set_raw_image(raw_image)

	def update_raw_rect(self, camera):
		# self.dirty = 1

		_, v = camera.world_to_pixel_coords(Vector3(-X_MAX, 0, 0), NOMINAL_RESOLUTION)
		size = (NOMINAL_RESOLUTION[0], NOMINAL_RESOLUTION[1] - v)

		raw_rect = pg.Rect((0, v), size)

		if self.raw_rect is None:
			return_rect = raw_rect
		else:
			x = 0
			y = min(raw_rect.y, self.raw_rect.y)
			w = self.raw_rect.w
			h = abs(raw_rect.y - self.raw_rect.y)
			return_rect = pg.Rect(x, y, w, h)
		self.set_raw_rect(raw_rect)

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
		r = None
		if cam.position.z != self.prev_camera_position.z or cam.focus_point.z != self.prev_cam_focus_point.z:
			self.prev_camera_position = Vector3(cam.position)
			self.prev_cam_focus_point = Vector3(cam.focus_point)

			r = [self.update_raw_rect(cam)]

			source_rect = get_scaled_rect_from(r[0], self._f_scale)
			print("source rect", source_rect)
			print("image clip", self.image.get_clip())
			source_rect.x = -(self.image.get_clip().x - source_rect.x)
			source_rect.y = -(self.image.get_clip().y - source_rect.y)

			self.source_rect = source_rect
			# r : rect to redraw
		else:
			self.source_rect = None

		# update scale
		f_scale = Engine.Display.display_manager.DisplayManager.get_instance().f_scale
		ScalableSprite.update(self, f_scale, raw_rects_to_redraw=r)


