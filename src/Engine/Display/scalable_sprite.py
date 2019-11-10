# encoding : UTF-8

import pygame as pg

import Engine


class ScalableSprite(pg.sprite.DirtySprite):
	"""
	Dirty Sprite Class with scaling features.
	"""
	objects = []
	_display_scale_factor = 1

	@staticmethod
	def get_display_scale_factor():
		return ScalableSprite._display_scale_factor

	@staticmethod
	def set_display_scale_factor(val):
		ScalableSprite._display_scale_factor = val
		for ob in ScalableSprite.objects:
			ob.display_scale_factor = val

	def __init__(self, *groups):
		pg.sprite.DirtySprite.__init__(self, *groups)

		self.rect_to_redraw = pg.Rect(0, 0, 0, 0)

		# refactor
		self._raw_rect = pg.Rect(0, 0, 0, 0)
		self._raw_image = pg.Surface((0, 0))

		self._scaled_rect = pg.Rect(0, 0, 0, 0)
		self._scaled_image = pg.Surface((0, 0))

		self._fit_size = None

		self._display_scale_factor = ScalableSprite.display_scale_factor

		# TODO: remove list: use ScalableSprite.display_scale_factor instead
		ScalableSprite.objects.append(self)

	@property
	def display_scale_factor(self):
		return self._display_scale_factor

	@display_scale_factor.setter
	def display_scale_factor(self, val):
		self._display_scale_factor = val
		self.rect = self._raw_rect
		self.image = self._raw_image

	@property
	def rect(self):
		return self._scaled_rect

	@rect.setter
	def rect(self, raw_val):
		self._raw_rect = raw_val
		if self._fit_size is not None and self._raw_rect.size != self._fit_size:
			self._raw_rect.w, self._raw_rect.h = self._fit_size

		self._scaled_rect = get_scaled_rect_from(raw_val, self.get_display_scale_factor())

	@property
	def image(self):
		return self._scaled_image

	@image.setter
	def image(self, raw_val):
		self._raw_image = raw_val
		if "_fit_size" in self.__dict__.keys():  # necessary if a class inherits from a class A and this class
			raw_size = raw_val.get_size() if self._fit_size is None else self._fit_size
		else:
			raw_size = raw_val.get_size()

		new_size = [self.get_display_scale_factor() * raw_size[i] for i in (0, 1)]
		self._scaled_image = pg.transform.scale(raw_val, new_size)

	def set_fit_size(self, new_size):
		"""
		Set fit size, to force to fit raw image and raw rect.

		If given new size is None, raw image size and raw rect size are used without any change.
		:param tuple(int, int) new_size: new size to fit
		:return: None
		"""
		if self._fit_size != new_size:
			self._fit_size = new_size
			self.image = self._raw_image
			self.rect = self._raw_rect

	def kill(self):
		pg.sprite.DirtySprite.kill(self)
		ScalableSprite.objects.remove(self)

	def update(self, *args):
		"""
		Update :var rect: and :var image: if needed.
		
		Rect and image are updated if scale factor changed or if sprite is dirty.
		
		:param pygame.Rect raw_rect_to_redraw:
		:return: None
		"""
		if len(args) == 1:
			raw_rect_to_redraw = args[0]
		else:
			raw_rect_to_redraw = None

		if self.dirty > 0:
			# rects to redraw
			if raw_rect_to_redraw is None:
				self.rect_to_redraw = self.rect.copy()
			else:
				self.rect_to_redraw = get_scaled_rect_from(raw_rect_to_redraw, self.get_display_scale_factor())
			# shift rect
			shift_rect_ip(self.rect_to_redraw)


def get_scaled_rect_from(raw_rect, scale_factor):
	"""
	Get rect scaled by scale factor, scaling x and y too.

	x, y, w and h of new scaled rect are integers.

	:param pygame.Rect raw_rect: rect before scaling
	:param float scale_factor: scale factor to use
	:return:scaled rect
	:rtype: pygame.Rect
	"""
	x, y = [int(scale_factor * raw_rect.topleft[i]) for i in (0, 1)]
	w, h = [int(scale_factor * raw_rect.size[i]) for i in (0, 1)]
	return pg.Rect((x, y), (w, h))


def shift_rect_ip(rect):
	"""
	Shift rect in place by avoiding negative coordinates for top-left pixel.

	:param pygame.Rect rect: rect to shift
	:return: None
	"""
	rect.w = max(0, rect.w + min(0, rect.x))
	rect.h = max(0, rect.h + min(0, rect.y))
	rect.x = max(0, rect.x)
	rect.y = max(0, rect.y)
