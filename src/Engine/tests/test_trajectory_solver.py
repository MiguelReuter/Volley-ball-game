# encoding : UTF-8

from pygame import *
from Engine.Trajectory import *


def test_find_target_position():
	origin_pos = Vector3(0, 1, 0)
	
	# vertical throw
	assert Vector3(0, 1, 1.5) == find_target_position(origin_pos, Vector3(0, 0, 10), wanted_z=1.5)
	
	# throw in XZ plane
	target_pos = find_target_position(origin_pos, Vector3(0, 2, 2), wanted_z=0)
	assert target_pos.x == origin_pos.x
	assert target_pos.y > origin_pos.y
	assert target_pos.z == 0

	# throw in 3D
	target_pos = find_target_position(origin_pos, Vector3(10, 2, 2), wanted_z=-0.5)
	assert target_pos.x > origin_pos.x
	assert target_pos.y > origin_pos.y
	assert target_pos.z == -0.5


def test_find_initial_velocity():
	origin_pos = Vector3(0, 1, 0)
	
	# throw along -y axis
	target_pos = Vector3(0, 0, 0)
	vel = find_initial_velocity(origin_pos, target_pos, wanted_height=1)
	assert vel.x == 0
	assert vel.y < 0
	assert vel.z > 0
	
	# throw along -y axis
	target_pos = Vector3(5, 1, 0)
	vel = find_initial_velocity(origin_pos, target_pos, wanted_height=1)
	assert vel.x > 0
	assert vel.y == 0
	assert vel.z > 0
	
	# throw in 3D
	target_pos = Vector3(-5, 3, 0.5)
	vel = find_initial_velocity(origin_pos, target_pos, wanted_height=1)
	assert vel.x < 0
	assert vel.y > 0
	assert vel.z > 0
	
	
def test_initial_velocity_and_target_position():
	origin_pos = Vector3(0, 1, 0)
	target_position = Vector3(0, 5, 0)
	
	initial_velocity = find_initial_velocity(origin_pos, target_position, wanted_height=1)
	assert target_position == find_target_position(origin_pos, initial_velocity, wanted_z=0)
	
	
def test_get_n_points_in_trajectory():
	origin_pos = Vector3(0, 1, 0)
	initial_velocity = Vector3(2, 0, 2)
	n = 10
	
	target_pos = find_target_position(origin_pos, initial_velocity, 0)
	
	points = get_n_points_in_trajectory(n, origin_pos, initial_velocity, wanted_z=0)
	
	assert len(points) == n
	assert points[0] == origin_pos
	assert points[n-1] == target_pos
	