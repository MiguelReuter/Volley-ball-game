# encoding : UTF-8

from enum import Enum
from pygame import *

# MAIN WINDOW
NOMINAL_RESOLUTION = (400, 320)
CAPTION_TITLE= "Volley-ball game"

class WindowMode(Enum):
	FIXED_SIZE = 0
	RESIZABLE = 1
	FULL_SCREEN = 2

WINDOW_MODE = WindowMode.RESIZABLE
WINDOW_RESIZE_2N = True  # ignored in full screen mode
"""
FIXED_SIZE, RESIZABLE, or FULL_SCREEN

if FIXED_SIZE :
	if WINDOW_RESIZE_2N:
		- window size = nominal_resolution * 2^n  (highest possible n)
	else:
		- window size = nominal_resolution
		
elif RESIZABLE:
	- initial window size = nominal_resolution or nominal_resolution * 2^n  according to WINDOW_RESIZE_2N
	- if window is resized ingame :
		- window content size = highest possible, centered content (float factor for size)
		
elif FULL_SCREEN
	- window content size = highest possible, centered content (float factor for size)

"""

# TIME
NOMINAL_FRAME_RATE = 30


# CAMERA
CAMERA_POS = (9, 0, 3)
FOCUS_POINT = (0, 0, 3)  # y component is ignored
FOV_ANGLE = 30.


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
