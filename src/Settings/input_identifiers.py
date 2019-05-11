# encoding : UTF-8

from collections import namedtuple

# Joystick
JoyHat = namedtuple("JoyHat", "hat_id value")
JoyAxis = namedtuple("JoyAxis", "axis value")
