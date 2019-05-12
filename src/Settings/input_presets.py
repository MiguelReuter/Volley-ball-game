# encoding : UTF-8

from pygame import *
from Settings.input_identifiers import *

# a dict for each input device (keyboard, joystick...)
# TODO : manage several keys for an action ? ex : CTRL + A for a specific action
INPUT_PRESET_KEYBOARD = \
	{"MOVE_LEFT": K_q,
	 "MOVE_RIGHT": K_d,
	 "MOVE_UP": K_z,
	 "MOVE_DOWN": K_s,
	 "THROW_BALL": K_j,
	 "JUMP": K_i,
	 "DIVE": K_l,
	 "CAMERA_MOVE_LEFT": K_LEFT,
	 "CAMERA_MOVE_RIGHT": K_RIGHT,
	 "CAMERA_MOVE_UP": K_UP,
	 "CAMERA_MOVE_DOWN": K_DOWN,
	 "QUIT": K_ESCAPE,
	 "PAUSE": K_p,
	 "SPACE_TEST": K_SPACE}


INPUT_PRESET_JOYSTICK = \
	{"MOVE_LEFT": Pov.LEFT,
	 "MOVE_RIGHT": Pov.RIGHT,
	 "MOVE_UP": Pov.UP,
	 "MOVE_DOWN": Pov.DOWN,
	 "THROW_BALL": 0,
	 "JUMP": 1,
	 "DIVE": 2,
	 "CAMERA_MOVE_LEFT": JoyAxis.LEFT_2,
	 "CAMERA_MOVE_RIGHT": JoyAxis.RIGHT_2,
	 "CAMERA_MOVE_UP": JoyAxis.UP_2,
	 "CAMERA_MOVE_DOWN": JoyAxis.DOWN_2,
	 "QUIT": 8,
	 "PAUSE": 9,
	 "SPACE_TEST": 3}
