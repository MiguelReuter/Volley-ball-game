# encoding: UTF-8

import pygame as pg
import json


class AnimatedSprite(pg.sprite.DirtySprite):
	class Frame:
		def __init__(self, frame_dict, sprite_sheet_image):
			self.frame_rect = pg.Rect(*[frame_dict["frame"][k] for k in ('x', 'y', 'w', 'h')])
			self.duration = frame_dict["duration"]
			self.image = sprite_sheet_image.subsurface(self.frame_rect)

	class Meta:
		def __init__(self, meta_dict):
			self.image_filename = meta_dict["image"]
			self.image_size = meta_dict["size"]
			self.frame_tags = meta_dict["frameTags"]

			self._app = meta_dict["app"]
			self._version = meta_dict["version"]
			self._image_format = meta_dict["format"]
			self._image_scale = meta_dict["scale"]

	class Animation:
		def __init__(self, frame_tag_dict, all_frames):
			self.name = frame_tag_dict["name"]
			self.frames = all_frames[frame_tag_dict["from"]:frame_tag_dict["to"]+1]
			self.direction = frame_tag_dict["direction"]

	def __init__(self, *groups):
		pg.sprite.DirtySprite.__init__(self, *groups)
		self.sprite_sheet = pg.Surface((0, 0))
		self.animations = {}
		self.current_animation = None
		self.current_frame = None

		self._prev_t = 0

		self.image = pg.Surface((0, 0))

	def load_aseprite_json(self, file):
		with open(file, mode='r') as json_file:
			data = json.load(json_file)

			meta = AnimatedSprite.Meta(data["meta"])

			self.sprite_sheet = pg.image.load(meta.image_filename).convert_alpha()

			# all frames
			_frames = []
			for f in data["frames"]:
				_frames.append(AnimatedSprite.Frame(f, self.sprite_sheet))

			# animations
			self.animations = {}
			for frame_tag in meta.frame_tags:
				self.animations[frame_tag["name"]] = AnimatedSprite.Animation(frame_tag, _frames)

	def play_animation(self, animation_name):
		self.current_animation = self.animations[animation_name]
		self.current_frame = self.current_animation.frames[0]
		self.image = self.current_frame.image
		
	def next_frame(self):
		# TODO: use generator
		i = self.current_animation.frames.index(self.current_frame)
		n = len(self.current_animation.frames)

		self.current_frame = self.current_animation.frames[(i + 1) % n]
		self.image = self.current_frame.image

	def update(self, *args):
		pg.sprite.DirtySprite.update(self, *args)

		t = pg.time.get_ticks()
		if t - self._prev_t > self.current_frame.duration:
			self._prev_t = t
			self.next_frame()


if __name__ == "__main__":
	def visualize_animation(aseprite_json, animation_name):
		"""
		Open window and play a specified animation.

		:param str aseprite_json: path to json
		:param str animation_name: name of animation to play
		:return:
		"""
		pg.init()

		screen = pg.display.set_mode((64, 64))

		animated_sprite = AnimatedSprite()
		animated_sprite.load_aseprite_json(aseprite_json)

		animated_sprite.play_animation(animation_name)

		# infinite loop, esc. to quit
		_done = False
		while not _done:
			for ev in pg.event.get():
				if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
					_done = True

			screen.fill((0, 0, 0))
			screen.blit(animated_sprite.image, animated_sprite.image.get_clip())
			animated_sprite.update()
			pg.display.flip()
		pg.quit()


	visualize_animation("/home/miguel/chicken_fox/chicken_array.json", "Idle")
