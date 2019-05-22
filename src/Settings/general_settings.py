# encoding : UTF-8

from enum import Enum
from pygame import *


# MAIN WINDOW
NOMINAL_RESOLUTION = (400, 320)
CAPTION_TITLE = "Volley-ball game"


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
	- if window is resized in-game :
		- window content size = highest possible, centered content (float factor for size)
		
elif FULL_SCREEN
	- window content size = highest possible, centered content (float factor for size)

"""

# TIME
NOMINAL_FRAME_RATE = 30
TIME_SPEED = 1  # < 1 to slow down, > 1 to speed up

# PHYSICS
G = 10

# CAMERA
CAMERA_POS = (11, 0, 3)
FOCUS_POINT = (0, 0, 3)
FOV_ANGLE = 60.

# WORLD
# court
COURT_DIM_X = 6
COURT_DIM_Y = 10
NET_HEIGHT_BTM = 1.5
NET_HEIGHT_TOP = 3

# ball
BALL_RADIUS = 0.5

# character
CHARACTER_W = 0.4
CHARACTER_H = 1


# INPUTS
class KeyState(Enum):
	RELEASED = 0
	JUST_PRESSED = 1
	PRESSED = 2
	JUST_RELEASED = 3


# PLAYER ACTIONS PARAMETERS
THROW_DURATION = 500    				# in ms
SERVE_DURATION = 500    				# in ms
JUMP_VELOCITY = 8       				# in m/s
SMASH_VELOCITY = 15     				# in m/s
DIVE_SPEED = 4							# in m/s
DIVE_SLIDE_DURATION = 250				# in ms
DIVE_DURATION_FOR_STANDING_UP = 500		# in ms

# THROW PARAMETERS
THROW_CENTER = Vector3(0, 3, BALL_RADIUS)
THROW_AMP_DIR = (2, 1.4)

SMASH_CENTER = Vector3(0, 4, BALL_RADIUS)
SMASH_AMP_DIR = (0, 1.4)

SERVE_CENTER = Vector3(0, 3.5, BALL_RADIUS)
SERVE_AMP_DIR = (2.4, 1.4)

DRAFT_THROW_HEIGHT = 4
DRAFT_DIRECTION_COEFFICIENT = 1.0

# events
ACTION_EVENT = USEREVENT + 1
THROW_EVENT = USEREVENT + 2


# throwing type
class ThrowingType(Enum):
	THROW = 0
	SMASH = 1
	SERVE = 2
	DRAFT = 3
	
	
# players id
class PlayerId(Enum):
	PLAYER_ID_ALL = 0
	PLAYER_ID_1 = 1
	PLAYER_ID_2 = 2

