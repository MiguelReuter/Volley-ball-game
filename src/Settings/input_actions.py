# encoding : UTF-8

from Settings.general_settings import *


# an unique dict for several input devices
INPUT_ACTIONS = \
	{PlayerAction.MOVE_LEFT: KeyState.PRESSED,
	 PlayerAction.MOVE_RIGHT: KeyState.PRESSED,
	 PlayerAction.MOVE_UP: KeyState.PRESSED,
	 PlayerAction.MOVE_DOWN: KeyState.PRESSED,
	 PlayerAction.THROW_BALL: KeyState.JUST_PRESSED,
	 PlayerAction.JUMP: KeyState.JUST_PRESSED,
	 PlayerAction.DIVE: KeyState.JUST_PRESSED,
	 PlayerAction.CAMERA_MOVE_LEFT: KeyState.PRESSED,
	 PlayerAction.CAMERA_MOVE_RIGHT: KeyState.PRESSED,
	 PlayerAction.CAMERA_MOVE_UP: KeyState.PRESSED,
	 PlayerAction.CAMERA_MOVE_DOWN: KeyState.PRESSED,
	 PlayerAction.QUIT: KeyState.JUST_PRESSED,
	 PlayerAction.PAUSE: KeyState.JUST_PRESSED,
	 PlayerAction.SPACE_TEST: KeyState.JUST_PRESSED}
