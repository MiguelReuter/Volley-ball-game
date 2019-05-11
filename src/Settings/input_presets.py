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
	 "CAMERA_MOVE_LEFT": K_LEFT,
	 "CAMERA_MOVE_RIGHT": K_RIGHT,
	 "CAMERA_MOVE_UP": K_UP,
	 "CAMERA_MOVE_DOWN": K_DOWN,
	 "QUIT": K_ESCAPE,
	 "PAUSE": K_p,
	 "SPACE_TEST": K_SPACE}


INPUT_PRESET_JOYSTICK = \
	{"MOVE_LEFT": JoyHat(0, (-1, 0)),
	 "MOVE_RIGHT": JoyHat(0, (1, 0)),
	 "MOVE_UP": JoyHat(0, (0, 1)),
	 "MOVE_DOWN": JoyHat(0, (0, -1)),
	 "THROW_BALL": 0,
	 "JUMP": 1,
	 "CAMERA_MOVE_LEFT": JoyAxis(2, -0.5),
	 "CAMERA_MOVE_RIGHT": JoyAxis(2, 0.5),
	 "CAMERA_MOVE_UP": JoyAxis(3, -0.5),
	 "CAMERA_MOVE_DOWN": JoyAxis(3, 0.5),
	 "QUIT": 8,
	 "PAUSE": 9,
	 "SPACE_TEST": 3}
