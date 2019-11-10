# encoding: UTF-8

import pygame as pg
import json


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
			- :var direction: :type float: direction of animation in ("forward", "backward")
		"""
		def __init__(self, frame_tag_dict, all_frames):
			self.name = frame_tag_dict["name"]
			self.frames = all_frames[frame_tag_dict["from"]:frame_tag_dict["to"]+1]
			self.direction = frame_tag_dict["direction"]

	def __init__(self, *groups):
		pg.sprite.DirtySprite.__init__(self, *groups)
		self.sprite_sheet = pg.Surface((0, 0))
		self.animations = {}
		self._current_animation = None

		self.image = pg.Surface((0, 0))

		self._animation_generator = None

	def load_aseprite_json(self, file):
		"""
		Load aseprite JSON file, containing animations and images.

		Tested with Libresprite v1.1.8.
		In Aseprite, when exporting sprite sheet :
			- check "JSON File"
			- choose "Array" (not "Hash")
			- check "Layers" and "Frame Tags" in Meta options

		:param str file: path of ase file
		:return: None
		"""
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
		"""
		Change current animation to the specified one.

		Desired animation must be in self.animations dict, else nothing is done.

		:param str animation_name:
		:return: None
		"""
		if animation_name in self.animations.keys():
			self._current_animation = self.animations[animation_name]
			self._animation_generator = self.play_generator()
			self.play_current_animation()
		else:
			print("{} not in {} animations".format(animation_name, self))

	def play_generator(self):
		"""
		Basic generator used to play current animation.

		This generator yields None and change :var self.image: if needed.

		:return: None
		"""
		i = 0
		n = len(self._current_animation.frames)
		prev_t = pg.time.get_ticks()

		_current_frame = self._current_animation.frames[i]
		self.image = _current_frame.image
		while 1:  # if loop
			curr_t = pg.time.get_ticks()

			if curr_t - prev_t > _current_frame.duration:
				# change current frame and image
				prev_t = curr_t

				if self._current_animation.direction == "forward":
					i = (i + 1) % n
				elif self._current_animation.direction == "backward":
					i = (i - 1) % n
				else:
					print("animation direction {} not implemented".format(self._current_animation.direction))

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


	class Foo(AnimatedSprite, ScalableSprite):
		"""
		Foo class for testing multiple inheritance with animated and scalable sprite.
		"""
		def __init__(self, *groups):
			AnimatedSprite.__init__(self, *groups)
			ScalableSprite.__init__(self, *groups)


	def visualize_animation(aseprite_json, animation_name=None):
		"""
		Open window and play animations.

		A list of animations name can be specified, or None for playing all animations contained in aseprite_json.
		A press on space bar key change current animation

		:param str aseprite_json: path to json
		:param str animation_name: name of animation to play. Could be:
			- :type str: to specify an unique animation
			- :type list(str): to specify several animations
			- None to play all animations
		:return:
		"""
		if isinstance(animation_name, str):
			animation_name = (animation_name, )

		i_anim = 0

		pg.init()

		screen = pg.display.set_mode((128, 128))

		animated_sprite = Foo()
		ScalableSprite.set_display_scale_factor(8)
		animated_sprite.load_aseprite_json(aseprite_json)

		if animation_name is None:
			animation_name = list(animated_sprite.animations.keys())

		animated_sprite.set_current_animation(animation_name[0])

		# infinite loop, esc. to quit
		_done = False
		while not _done:
			for ev in pg.event.get():
				if ev.type == pg.KEYDOWN:
					if ev.key == pg.K_ESCAPE:
						_done = True
					elif ev.key == pg.K_SPACE:
						i_anim = (i_anim + 1) % len(animation_name)
						animated_sprite.set_current_animation(animation_name[i_anim])
						print("set {} animation".format(animation_name[i_anim]))

			screen.fill((0, 0, 0))
			animated_sprite.update()
			screen.blit(animated_sprite.image, animated_sprite.image.get_clip())
			pg.display.flip()
		pg.quit()


	visualize_animation("../../../assets/sprites/animation_test.json")



