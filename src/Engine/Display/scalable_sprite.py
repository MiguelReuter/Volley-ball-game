# encoding : UTF-8

import pygame as pg


class ScalableSprite(pg.sprite.DirtySprite):
	"""
	Dirty Sprite Class with scaling features.
	"""
	def __init__(self, scale_factor, *groups):
		pg.sprite.DirtySprite.__init__(self, *groups)
		self._f_scale = scale_factor
		
		self.raw_rect = pg.Rect((0, 0), (0, 0))
		self.raw_image = pg.Surface((0, 0))
		
		self.rect = pg.Rect((0, 0), (0, 0))
		self.image = pg.Surface((0, 0))

		self.rect_list_to_redraw = []
		self.rect_list_to_erase = []

	def set_raw_rect(self, raw_rect):
		"""
		Set raw rect and update scaled :val rect: attribute.
		
		:param pygame.Rect raw_rect: new raw rect
		:return: None
		"""
		self.raw_rect = raw_rect
		self.rect = get_scaled_rect_from(raw_rect, self._f_scale)

	def set_raw_image(self, raw_image):
		"""
		Set raw rect and update scaled :val image: attribute.

		:param pygame.Surface raw_image: new raw image
		:return: None
		"""
		self.raw_image = raw_image
		
		new_size = [int(self._f_scale * raw_image.get_size()[i]) for i in (0, 1)]
		self.image = pg.Surface(new_size)
		self.image = pg.transform.scale(raw_image, new_size)
	
	def update(self, new_scale_factor=None, raw_rects_to_redraw=None, raw_rects_to_erase=None):
		"""
		Update :var rect: and :var image: if needed.
		
		Rect and image are updated if scale factor changed or if sprite is dirty.
		
		:param float new_scale_factor: new scaling factor to use
		:param list(pygame.Rect) raw_rects_to_redraw:
		:param list(pygame.Rect) raw_rects_to_erase:
		:return: None
		"""
		if self.dirty > 0:
			# rects to redraw
			if raw_rects_to_redraw is None:
				self.rect_list_to_redraw = [self.rect.copy()]
			else:
				self.rect_list_to_redraw = [get_scaled_rect_from(r, self._f_scale) for r in raw_rects_to_redraw]

		if new_scale_factor is not None and new_scale_factor != self._f_scale:
			self.dirty = 1
			self._f_scale = new_scale_factor
			
			# image
			new_size = [int(self._f_scale * self.raw_image.get_size()[i]) for i in (0, 1)]
			self.image = pg.Surface(new_size)
			self.image = pg.transform.scale(self.raw_image, new_size)
			
			# rect
			self.rect = get_scaled_rect_from(self.raw_rect, self._f_scale)
			self.rect_list_to_redraw = [self.rect.copy()]

		# rects to erase
		if raw_rects_to_erase is not None:
			self.rect_list_to_erase = [get_scaled_rect_from(r, self._f_scale) for r in raw_rects_to_erase]


def get_scaled_rect_from(raw_rect, scale_factor):
	x, y = [int(scale_factor * raw_rect.topleft[i]) for i in (0, 1)]
	w, h = [int(scale_factor * raw_rect.size[i]) for i in (0, 1)]
	return pg.Rect((x, y), (w, h))
