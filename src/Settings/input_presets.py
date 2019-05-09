# encoding : UTF-8

from pygame import *


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
