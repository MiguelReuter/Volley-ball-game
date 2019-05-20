# encoding : UTF-8

from Settings.general_settings import *


# an unique dict for several input devices
INPUT_ACTIONS = \
	{"MOVE_LEFT": KeyState.PRESSED,
	 "MOVE_RIGHT": KeyState.PRESSED,
	 "MOVE_UP": KeyState.PRESSED,
	 "MOVE_DOWN": KeyState.PRESSED,
	 "THROW_BALL": KeyState.JUST_PRESSED,
	 "JUMP": KeyState.JUST_PRESSED,
	 "DIVE": KeyState.JUST_PRESSED,
	 "CAMERA_MOVE_LEFT": KeyState.PRESSED,
	 "CAMERA_MOVE_RIGHT": KeyState.PRESSED,
	 "CAMERA_MOVE_UP": KeyState.PRESSED,
	 "CAMERA_MOVE_DOWN": KeyState.PRESSED,
	 "QUIT": KeyState.JUST_PRESSED,
	 "PAUSE": KeyState.JUST_PRESSED,
	 "SPACE_TEST": KeyState.JUST_PRESSED}
