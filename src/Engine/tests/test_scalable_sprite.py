# encoding : UTF-8

from Engine.Display.scalable_sprite import shift_rect_ip
from pygame import Rect


def test_shift_rect_ip():
	# 1
	rect = Rect(0, 0, 10, 10)
	shift_rect_ip(rect)
	assert rect.x == 0
	assert rect.y == 0
	assert rect.w == 10
	assert rect.h == 10

	# 2
	rect = Rect(-5, 2, 10, 10)
	shift_rect_ip(rect)
	assert rect.x == 0
	assert rect.y == 2
	assert rect.w == 5
	assert rect.h == 10

	# 3
	rect = Rect(2, -5, 10, 10)
	shift_rect_ip(rect)
	assert rect.x == 2
	assert rect.y == 0
	assert rect.w == 10
	assert rect.h == 5

	# 4
	rect = Rect(-25, 2, 10, 10)
	shift_rect_ip(rect)
	assert rect.x == 0
	assert rect.y == 2
	assert rect.w == 0
	assert rect.h == 10

