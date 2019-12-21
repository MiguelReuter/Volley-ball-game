# encoding : UTF-8

from enum import Enum


class AnimationDirectionEnum(str, Enum):
	FORWARD = "forward"
	REVERSE = "reverse"
	PINGPONG = "pingpong"
	RANDOM = "random"
