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
		
		self.prev_rect = pg.Rect((0, 0), (0, 0))
	
	def set_raw_rect(self, raw_rect):
		"""
		Set raw rect and update scaled :val rect: attribute.
		
		:param pygame.Rect raw_rect: new raw rect
		:return: None
		"""
		self.raw_rect = raw_rect
		
		x, y = [int(self._f_scale * raw_rect.topleft[i]) for i in (0, 1)]
		w, h = [int(self._f_scale * raw_rect.size[i]) for i in (0, 1)]
		self.rect = pg.Rect((x, y), (w, h))
	
	def set_raw_image(self, raw_image):
		"""
		Set raw rect and update scaled :val image: attribute.

		:param pygame.Rect raw_image: new raw image
		:return: None
		"""
		self.raw_image = raw_image
		
		new_size = [int(self._f_scale * raw_image.get_clip()[i]) for i in (0, 1)]
		self.image = pg.Surface(new_size)
		self.image = pg.transform.scale(raw_image, new_size)
	
	def update(self, new_scale_factor=None):
		"""
		Update :var rect: and :var image: if needed.
		
		Rect and image are updated if scale factor changed or if sprite is dirty.
		
		:param float new_scale_factor: new scaling factor to use
		:return: None
		"""
		if new_scale_factor is not None and new_scale_factor != self._f_scale or self.dirty > 0:
			self.dirty = 1
			self._f_scale = new_scale_factor
			
			# image
			new_size = [int(self._f_scale * self.raw_image.get_size()[i]) for i in (0, 1)]
			self.image = pg.Surface(new_size)
			self.image = pg.transform.scale(self.raw_image, new_size)
			
			# rect
			x, y = [int(self._f_scale * self.raw_rect.topleft[i]) for i in (0, 1)]
			self.prev_rect = self.rect
			self.rect = pg.Rect((x, y), self.image.get_size())
