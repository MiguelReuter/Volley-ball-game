from pygame import *

from Engine.utils import Collisions


def test_spheres_collisions():
	assert Collisions.are_spheres_colliding(Vector3(0, 0, 0), 1, Vector3(2, 0, 0), 1) is True
	assert Collisions.are_spheres_colliding(Vector3(0, 0, 0), 1, Vector3(2.001, 0, 0), 1) is False
	assert Collisions.are_spheres_colliding(Vector3(0, 0, 0), 1, Vector3(2, 0, 0), 0.5) is False

def test_sphere_and_aabb_collisions():
	sp_center = Vector3(0, 0, 0)
	sp_r = 1
	aabb_size3 = Vector3(2, 2, 2)
	
	assert Collisions.are_sphere_and_AABB_colliding(sp_center, sp_r, Vector3(2, 0, 0), aabb_size3) is True
	assert Collisions.are_sphere_and_AABB_colliding(sp_center, sp_r, Vector3(2.001, 0, 0), aabb_size3) is False
	
	
def test_aabb_collisions():
	center_a = Vector3(0, 0, 0)
	center_b = Vector3(2, 0, 0)
	size3_a = Vector3(2, 2, 2)
	size3_b = Vector3(2, 2, 2)
	
	assert Collisions.are_AABB_colliding(center_a, size3_a, center_b, size3_b) is True
	assert Collisions.are_AABB_colliding(center_a, size3_a, center_b+(0.1, 0, 0), size3_b) is False
