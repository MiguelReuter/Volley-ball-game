# encoding : UTF-8

from collections import namedtuple
from enum import Enum


# Joystick
JoyHatRaw = namedtuple("JoyHatRaw", "hat_id value")
JoyAxisRaw = namedtuple("JoyAxisRaw", "axis value")


class Pov(Enum):
	LEFT = JoyHatRaw(0, (-1, 0))
	RIGHT = JoyHatRaw(0, (1, 0))
	UP = JoyHatRaw(0, (0, 1))
	DOWN = JoyHatRaw(0, (0, -1))


JOY_AXIS_THRESHOLD = 0.4


class JoyAxis(Enum):
	# for left joystick
	LEFT_1 = JoyAxisRaw(0, -JOY_AXIS_THRESHOLD)
	RIGHT_1 = JoyAxisRaw(0, JOY_AXIS_THRESHOLD)
	UP_1 = JoyAxisRaw(1, -JOY_AXIS_THRESHOLD)
	DOWN_1 = JoyAxisRaw(1, JOY_AXIS_THRESHOLD)

	# for right joystick
	LEFT_2 = JoyAxisRaw(2, -JOY_AXIS_THRESHOLD)
	RIGHT_2 = JoyAxisRaw(2, JOY_AXIS_THRESHOLD)
	UP_2 = JoyAxisRaw(3, -JOY_AXIS_THRESHOLD)
	DOWN_2 = JoyAxisRaw(3, JOY_AXIS_THRESHOLD)


