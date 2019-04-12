# encoding : UTF-8

from enum import Enum
from pygame import *

# MAIN WINDOW
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
CAPTION_TITLE= "Volley-ball game"


# TIME
NOMINAL_FRAME_RATE = 30


# CAMERA
CAMERA_POS = (9, 0, 3)
FOCUS_POINT = (0, 0, 3)  # y component is ignored
FOV_ANGLE = 60.


# INPUTS
class KeyState(Enum):
	RELEASED = 0
	JUST_PRESSED = 1
	PRESSED = 2
	JUST_RELEASED = 3

# keyboard keys used in game (other keys are ignored)
KEYS = (K_z, K_s, K_q, K_d,
        K_UP, K_DOWN, K_LEFT, K_RIGHT,
        K_ESCAPE,
        K_SPACE,
        K_p)

# events
ACTIONEVENT = USEREVENT + 1
