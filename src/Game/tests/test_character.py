# encoding : UTF-8

from Game.character import Character
from pygame import Vector3

import pytest


@pytest.fixture()
def character():
	return Character(Vector3(), max_velocity=4)


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


def test_change_collider(character):
	char_original_pos = Vector3(character.position)
	char_original_collider_rel_pos = Vector3(character.collider_relative_position)
	coll_original_size = Vector3(character.collider.size3)
	coll_original_center = Vector3(character.collider.center)

	# set default collider
	character.set_default_collider()
	assert character.collider.size3 == coll_original_size
	assert character.collider.center == coll_original_center
	assert character.position == char_original_pos
	assert character.collider_relative_position == char_original_collider_rel_pos

	# change and reset collider
	direction = Vector3(0, 1, 0)
	character.set_diving_collider(direction)
	character.set_default_collider()
	assert character.collider.size3 == coll_original_size
	assert character.collider.center == coll_original_center
	assert character.position == char_original_pos
	assert character.collider_relative_position == char_original_collider_rel_pos

	# move, change collider, move again and reset collider
	direction = Vector3(0, 1, 0)

	character.move(Vector3(1, 0, 0), 1000)
	character.set_diving_collider(direction)
	character.move(Vector3(0, 1, 0), 500)
	character.set_default_collider()
	assert character.collider.size3 == coll_original_size
	assert character.collider.center == coll_original_center + character.max_velocity * Vector3(1, 0.5, 0)
	assert character.position == char_original_pos + character.max_velocity * Vector3(1, 0.5, 0)
	assert character.collider_relative_position == char_original_collider_rel_pos



