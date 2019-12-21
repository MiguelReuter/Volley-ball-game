# encoding : UTF-8

from Engine.Display.scalable_sprite import shift_rect_ip, get_scaled_rect_from
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


def test_get_scaled_rect():
	rect = Rect(3, 7, 5, 10)

	# 1
	scaled_rect = get_scaled_rect_from(rect, 2)
	assert scaled_rect.x == 6
	assert scaled_rect.y == 14
	assert scaled_rect.w == 10
	assert scaled_rect.h == 20

	# 2
	scaled_rect = get_scaled_rect_from(rect, 1)
	assert rect == scaled_rect

	# 3
	scaled_rect = get_scaled_rect_from(rect, 1/3)
	assert scaled_rect.x == 3//3
	assert scaled_rect.y == 7//3
	assert scaled_rect.w == 5//3
	assert scaled_rect.h == 10//3



