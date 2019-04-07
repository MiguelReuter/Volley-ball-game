# encoding : UTF-8

from enum import Enum
from pygame import *

# MAIN WINDOW
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
CAPTION_TITLE= "Volley-ball game"


# TIME
NOMINAL_FRAME_RATE = 30


# 3D DEBUG
# flags
SIZE_INDEPENDENT_FROM_Y_POS = True
SIZE_INDEPENDENT_FROM_Z_POS = False
# colors
DBG_COLOR_LINE = (100, 100, 255)
DBG_COLOR_SPHERE = (200, 0, 0)
DBG_COLOR_POLYGON = (200, 200, 200)
DBG_COLOR_AAB = (0, 200, 200)
DBG_COLOR_SHADOW = (20, 20, 20)
DBG_COLOR_SHADOW_TRAPEZE = (255, 0, 255)


# CAMERA
CAMERA_POS = (9, 0, 3)
FOCUS_POINT = (0, 0, 3)  # y component is ignored
FOV_ANGLE = 30.


# INPUTS
class KeyState(Enum):
	UNPRESSED = 0
	JUST_PRESSED = 1
	PRESSED = 2
	JUST_RELEASE = 3

# keyboard keys used in game (other keys are ignored)
KEYS = (K_z, K_s, K_q, K_d,
        K_UP, K_DOWN, K_LEFT, K_RIGHT,
        K_ESCAPE,
        K_SPACE,
        K_p)
