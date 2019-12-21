# encoding: UTF-8

import pygame as pg
import json
from random import randint

import Engine
from .utils import *


class AnimatedSprite(pg.sprite.DirtySprite):
	"""
	Class for animated sprite.

	Loading sprites and animations from file is supported for Aseprite software (v1.1.8), more details in
	load_aseprite_json method.

	A derived class can be created with ScalableSprite class features:
	>
	> class Foo(AnimatedSprite, ScalableSprite):  # note Class inheritance order.
	>	 # your code
	>	 pass

	"""

	class Frame:
		"""
		Frame objects are only defined by the following attributes:
			- :var frame_rect: :type pygame.Rect: corresponding portion of a sprite sheet image.
			- :var duration: :type int: duration of the frame in ms
			- :var image: :type pygame.Surface: sub image of corresponding sprite sheet image
		"""
		def __init__(self, frame_dict, sprite_sheet_image):
			self.frame_rect = pg.Rect(*[frame_dict["frame"][k] for k in ('x', 'y', 'w', 'h')])
			self.duration = frame_dict["duration"]
			self.image = sprite_sheet_image.subsurface(self.frame_rect)

	class Meta:
		"""
		Meta information contained in ase JSON file.
		"""
		def __init__(self, meta_dict):
			self.image_filename = meta_dict["image"]
			self.image_size = meta_dict["size"]
			self.frame_tags = meta_dict["frameTags"]

			self._app = meta_dict["app"]
			self._version = meta_dict["version"]
			self._image_format = meta_dict["format"]
			self._image_scale = meta_dict["scale"]

	class Animation:
		"""
		Animation objects are only defined by the following attributes:
			- :var name: :type str: name of animation
			- :var frames: :type list of Frame objects: list of animation's frames
			- :var direction: :type float: direction of animation in AnimationDirectionEnum
		"""
		def __init__(self, frame_tag_dict, all_frames, **kwargs):
			self.name = frame_tag_dict["name"]
			self.frames = all_frames[frame_tag_dict["from"]:frame_tag_dict["to"]+1]
			self.direction = AnimationDirectionEnum(frame_tag_dict["direction"])

			if "duration" in kwargs.keys():
				self.set_frame_duration(kwargs["duration"])

		def set_frame_duration(self, duration):
			"""
			Set duration for all frames.

			Duration is in ms. A list of int can be passed, each value corresponds to a frame.
			An int can also be passed to set an unique duration for all frames.

			:param [list|int] duration: list or an int containing frames' duration.
			"""

			if isinstance(duration, int) or isinstance(duration, float):
				for fr in self.frames:
					fr.duration = int(duration)
			elif isinstance(duration, list):
				n_values = len(duration)
				for i, fr in enumerate(self.frames):
					fr.duration = int(duration[i % n_values])

		def set_direction(self, new_direction):
			if new_direction in AnimationDirectionEnum:
				self.direction = new_direction
			else:
				print(new_direction + "not in" + AnimationDirectionEnum)

	def __init__(self, *groups):
		pg.sprite.DirtySprite.__init__(self, *groups)
		self.sprite_sheet = pg.Surface((0, 0))
		self.animations = {}
		self._speed_factor = 1.0
		self._current_animation = None
		self._animation_generator = None

	def load_aseprite_json(self, file):
		"""
		Load aseprite JSON file, containing animations and images.

		Load animations and images defined in JSON file. Set current animation to a random one.
		Tested with Libresprite v1.1.8.
		In Aseprite, when exporting sprite sheet :
			- check "JSON Data"
			- choose "Array" (not "Hash")
			- check "Layers" and "Frame Tags" in Meta options

		:param str file: path of ase file
		:return: None
		"""
		with open(file, mode='r') as json_file:
			data = json.load(json_file)

			# load meta data and sprite sheet
			meta = AnimatedSprite.Meta(data["meta"])
			self.sprite_sheet = pg.image.load(meta.image_filename).convert_alpha()

			# load all frames
			_frames = []
			for f in data["frames"]:
				_frames.append(AnimatedSprite.Frame(f, self.sprite_sheet))

			# load animations, with frames and images
			self.animations = {}
			if len(meta.frame_tags) == 0:
				print("No frame tags in {} !".format(file))

			for frame_tag in meta.frame_tags:
				self.animations[frame_tag["name"]] = AnimatedSprite.Animation(frame_tag, _frames)

			self.set_current_animation()

	def set_current_animation(self, animation_name=None, **kwargs):
		"""
		Change current animation to the specified one.

		Desired animation must be in self.animations dict, else nothing is done.
		'duration' can be specified to set currant animation frames' duration according to the
		AnimatedSprite.Animation.set_frame_duration method.

		:param str animation_name:
		:param **dict kwargs: 'duration' for frames' duration
		:return: None
		"""
		if animation_name is None:
			animation_name = list(self.animations.keys())[0]

		if animation_name in self.animations.keys():
			self._current_animation = self.animations[animation_name]
			if "duration" in kwargs.keys():
				self._current_animation.set_frame_duration(kwargs["duration"])

			self._animation_generator = self.play_generator()
			self.play_current_animation()
		else:
			print("{} not in {} animations".format(animation_name, self))

	def get_current_animation(self):
		return self._current_animation

	def set_speed(self, val):
		self._speed_factor = val

	def play_generator(self):
		"""
		Basic generator used to play current animation.

		This generator yields None and change :var self.image: if needed. If a frame has a duration of '0', animation
		will be stopped on this frame, until duration is changed.
		"""
		def get_ticks():
			if Engine.GameEngine.get_instance() is not None:
				# TODO: play animation when game is paused ?
				return Engine.GameEngine.get_instance().get_running_ticks()
			else:
				return pg.time.get_ticks()

		i = 0
		n = len(self._current_animation.frames)
		prev_t = get_ticks()

		if self._current_animation.direction == AnimationDirectionEnum.REVERSE:
			_low_to_high = False
		else:
			_low_to_high = True

		if self._current_animation.direction not in AnimationDirectionEnum:
			print("animation direction {} not implemented".format(self._current_animation.direction))

		_current_frame = self._current_animation.frames[i]
		self.image = _current_frame.image
		while 1:  # if loop
			curr_t = get_ticks()

			if self._speed_factor * (curr_t - prev_t) > _current_frame.duration > 0:
				self.dirty = 1
				# change current frame and image
				prev_t = curr_t

				if _low_to_high:
					i = (i + 1) % n
				else:
					i = (i - 1) % n
				if self._current_animation.direction == AnimationDirectionEnum.PINGPONG:
					if i == n - 1 or i == 0:
						_low_to_high = not _low_to_high
				elif self._current_animation.direction == AnimationDirectionEnum.RANDOM and n >= 2:
					i = (i + randint(0, n - 2)) % n  # prevent to have 2 same images in a row

				_current_frame = self._current_animation.frames[i]
				self.image = _current_frame.image
			yield None

	def play_current_animation(self):
		"""
		Play current animation.

		:return: None
		"""
		self._animation_generator.__next__()

	def update(self, *args):
		pg.sprite.DirtySprite.update(self, *args)
		self.play_current_animation()


if __name__ == "__main__":
	from Engine.Display.scalable_sprite import ScalableSprite


	class AnimatedAndScalableSpriteTest(AnimatedSprite, ScalableSprite):
		"""
		Class for testing multiple inheritance with animated and scalable sprite.
		"""
		def __init__(self, *groups):
			AnimatedSprite.__init__(self, *groups)
			ScalableSprite.__init__(self, *groups)


	def visualize_animations(aseprite_json, animation_name=None):
		"""
		Open window and play animations.

		A list of animations name can be specified, or None for playing all animations contained in aseprite_json.
		A press on space bar key change current animation.

		:param str aseprite_json: path to json
		:param str animation_name: name of animation to play. Could be:
			- :type str: to specify an unique animation
			- :type list(str): to specify several animations
			- None to play all animations
		:return:
		"""
		pg.init()

		screen = pg.display.set_mode((128, 128))

		animated_sprite = AnimatedAndScalableSpriteTest()
		ScalableSprite.set_display_scale_factor(16)
		animated_sprite.load_aseprite_json(aseprite_json)

		if isinstance(animation_name, str):
			animation_name = (animation_name, )
		elif animation_name is None:
			animation_name = list(animated_sprite.animations.keys())

		i_anim = 0
		animated_sprite.set_current_animation(animation_name[i_anim])
		print("set {} animation".format(animation_name[i_anim]))

		# infinite loop, esc. to quit
		_done = False
		while not _done:
			for ev in pg.event.get():
				if ev.type == pg.KEYDOWN:
					if ev.key == pg.K_ESCAPE:
						_done = True

					# change current animation
					elif ev.key == pg.K_SPACE:
						i_anim = (i_anim + 1) % len(animation_name)
						animated_sprite.set_current_animation(animation_name[i_anim])
						print("set {} animation".format(animation_name[i_anim]))

			# clean screen and blit image
			screen.fill((0, 0, 0))
			animated_sprite.update()
			screen.blit(animated_sprite.image, animated_sprite.image.get_clip())
			pg.display.flip()
		pg.quit()


	visualize_animations("../../../assets/sprites/animation_test.json")



