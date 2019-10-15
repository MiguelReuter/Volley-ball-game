# encoding : UTF-8

from Game.character import Character
from pygame import Vector3

import pytest


@pytest.fixture()
def character():
	return Character(Vector3(), max_velocity=4, jump_velocity=8)


def test_move_rel(character):
	assert character.position == Vector3()
	assert character.collider.center == Vector3() + character.collider_relative_position

	# move
	character.move_rel(Vector3(0, 1, 0.1), free_displacement=True)
	assert character.position == Vector3(0, 1, 0.1)
	assert character.collider.center == Vector3(0, 1, 0.1) + character.collider_relative_position

	# move
	character.move_rel(Vector3(-0.2, 0, 0), free_displacement=True)
	assert character.position == Vector3(-0.2, 1, 0.1)
	assert character.collider.center == Vector3(-0.2, 1, 0.1) + character.collider_relative_position


def test_move(character):
	direction = Vector3(1, 0, 0)
	dt = 1000

	# move
	character.move(direction, dt, free_displacement=True)
	assert character.position == Vector3(4, 0, 0)
	assert character.collider.center == Vector3(4, 0, 0) + character.collider_relative_position

	# move
	direction = Vector3(0, 2, 0)
	character.move(direction, dt, free_displacement=True)
	assert character.position == Vector3(4, 8, 0)
	assert character.collider.center == Vector3(4, 8, 0) + character.collider_relative_position


def test_move_time(character):
	dt = 10

	origin_pos = Vector3()
	character.position = Vector3(origin_pos)

	n = 100
	# move along +y axis for n frames
	for _ in range(n):
		character.move(Vector3(0, 1, 0), dt, free_displacement=True)
	assert n * dt / 1000 == pytest.approx(character.get_time_to_run_to(origin_pos), 0.01)

	# move along +x +y axis for n frames
	for _ in range(n):
		character.move(Vector3(0.7071, 0.7071, 0), dt, free_displacement=True)

	assert 2 * n * dt / 1000 == pytest.approx(character.get_time_to_run_to(origin_pos), 0.01)


def test_jump_time(character):
	# jump
	character.velocity.z = character.jump_velocity

	# height
	h = 2

	dt = 10
	for i in range(100):
		character.update_physics(dt, free_displacement=True)
		if character.position.z + character.h > h:
			break

	assert i * dt / 1000 == pytest.approx(character.get_time_to_jump_to_height(h), 0.1)


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

	character.move(Vector3(1, 0, 0), 1000, free_displacement=True)
	character.set_diving_collider(direction)
	character.move(Vector3(0, 1, 0), 500, free_displacement=True)
	character.set_default_collider()
	assert character.collider.size3 == coll_original_size
	assert character.collider.center == coll_original_center + character.max_velocity * Vector3(1, 0.5, 0)
	assert character.position == char_original_pos + character.max_velocity * Vector3(1, 0.5, 0)
	assert character.collider_relative_position == char_original_collider_rel_pos



