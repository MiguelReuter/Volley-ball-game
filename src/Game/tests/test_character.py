# encoding : UTF-8

from Game.character import *

import pytest


@pytest.fixture()
def character():
	return Character(Vector3(), w=0.4, h=1, max_velocity=4)


def test_move_rel(character):
	assert character.position == Vector3()
	assert character.collider.center == Vector3() + character.collider_relative_position

	# move
	character.move_rel(Vector3(0, 1, 0.1))
	assert character.position == Vector3(0, 1, 0.1)
	assert character.collider.center == Vector3(0, 1, 0.1) + character.collider_relative_position

	# move
	character.move_rel(Vector3(-0.2, 0, 0))
	assert character.position == Vector3(-0.2, 1, 0.1)
	assert character.collider.center == Vector3(-0.2, 1, 0.1) + character.collider_relative_position


def test_move(character):
	direction = Vector3(1, 0, 0)
	dt = 1000

	# move
	character.move(direction, dt)
	assert character.position == Vector3(4, 0, 0)
	assert character.collider.center == Vector3(4, 0, 0) + character.collider_relative_position

	# move
	direction = Vector3(0, 2, 0)
	character.move(direction, dt)
	assert character.position == Vector3(4, 8, 0)
	assert character.collider.center == Vector3(4, 8, 0) + character.collider_relative_position


