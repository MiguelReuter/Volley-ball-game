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
			self._generator = None

		def init(self):
			"""
			Call this when changing current animation to this one
			:return:
			"""
			self._generator = self.play_generator()

		def play_generator(self):
			# generator who yields image
			i = 0
			n = len(self.frames)
			prev_t = pg.time.get_ticks()

			_current_frame = self.frames[i]
			while 1:  # if loop
				curr_t = pg.time.get_ticks()

				if curr_t - prev_t > _current_frame.duration:
					prev_t = curr_t

					if self.direction == "forward":
						i = (i + 1) % n
					else:
						print("animation direction {} not implemented".format(self.direction))

					_current_frame = self.frames[i]
				yield _current_frame.image

		def play(self):
			return self._generator.__next__()

	def __init__(self, *groups):
		pg.sprite.DirtySprite.__init__(self, *groups)
		self.sprite_sheet = pg.Surface((0, 0))
		self.animations = {}
		self._current_animation = None

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

	def set_current_animation(self, animation_name):
		self._current_animation = self.animations[animation_name]
		self._current_animation.init()
		self.image = self._current_animation.play()

	def update(self, *args):
		pg.sprite.DirtySprite.update(self, *args)

		self.image = self._current_animation.play()


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

		animated_sprite.set_current_animation(animation_name)

		# infinite loop, esc. to quit
		_done = False
		while not _done:
			for ev in pg.event.get():
				if ev.type == pg.KEYDOWN:
					if ev.key == pg.K_ESCAPE:
						_done = True
					elif ev.key == pg.K_SPACE:
						animated_sprite.set_current_animation("Flying")

			screen.fill((0, 0, 0))
			screen.blit(animated_sprite.image, animated_sprite.image.get_clip())
			animated_sprite.update()
			pg.display.flip()
		pg.quit()


	visualize_animation("/home/miguel/chicken_fox/chicken_array.json", "Idle")
