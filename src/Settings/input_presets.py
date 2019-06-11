# encoding : UTF-8

from pygame.locals import *
from Settings.input_identifiers import *
from Settings.general_settings import PlayerAction

# a dict for each input device (keyboard, joystick...)
# TODO : manage several keys for an action ? ex : CTRL + A for a specific action
INPUT_PRESET_KEYBOARD = \
	{PlayerAction.MOVE_LEFT:            K_q,
	 PlayerAction.MOVE_RIGHT:           K_d,
	 PlayerAction.MOVE_UP:              K_z,
	 PlayerAction.MOVE_DOWN:            K_s,
	 PlayerAction.THROW_BALL:           K_j,
	 PlayerAction.JUMP:                 K_i,
	 PlayerAction.DIVE:                 K_l,
	 PlayerAction.CAMERA_MOVE_LEFT:     K_LEFT,
	 PlayerAction.CAMERA_MOVE_RIGHT:    K_RIGHT,
	 PlayerAction.CAMERA_MOVE_UP:       K_UP,
	 PlayerAction.CAMERA_MOVE_DOWN:     K_DOWN,
	 PlayerAction.QUIT:                 K_ESCAPE,
	 PlayerAction.PAUSE:                K_p,
	 PlayerAction.SPACE_TEST:           K_SPACE}


INPUT_PRESET_JOYSTICK = \
	{PlayerAction.MOVE_LEFT:            Pov.LEFT,
	 PlayerAction.MOVE_RIGHT:           Pov.RIGHT,
	 PlayerAction.MOVE_UP:              Pov.UP,
	 PlayerAction.MOVE_DOWN:            Pov.DOWN,
	 PlayerAction.THROW_BALL:           0,
	 PlayerAction.JUMP:                 1,
	 PlayerAction.DIVE:                 2,
	 PlayerAction.CAMERA_MOVE_LEFT:     JoyAxis.LEFT_2,
	 PlayerAction.CAMERA_MOVE_RIGHT:    JoyAxis.RIGHT_2,
	 PlayerAction.CAMERA_MOVE_UP:       JoyAxis.UP_2,
	 PlayerAction.CAMERA_MOVE_DOWN:     JoyAxis.DOWN_2,
	 PlayerAction.QUIT:                 8,
	 PlayerAction.PAUSE:                9,
	 PlayerAction.SPACE_TEST:           3}
