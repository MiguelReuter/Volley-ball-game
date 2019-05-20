# encoding : UTF-8

from Engine.Collisions import *


def test_spheres_collisions():
	sphere_a = SphereCollider(Vector3(0, 0, 0), 1)
	sphere_b = SphereCollider(Vector3(2, 0, 0), 1)

	assert are_spheres_colliding(sphere_a, sphere_b) is True
	
	sphere_b.center = Vector3(2.001, 0, 0)
	assert are_spheres_colliding(sphere_a, sphere_b) is False
	
	sphere_b.center = Vector3(2, 0, 0)
	sphere_b.radius = 0.5
	assert are_spheres_colliding(sphere_a, sphere_b) is False


def test_sphere_and_aabb_collisions():
	sphere = SphereCollider(Vector3(0, 0, 0), 1)
	aabb = AABBCollider(Vector3(2, 0, 0), Vector3(2, 2, 2))
	
	assert are_sphere_and_aabb_colliding(sphere, aabb) is True
	
	aabb.center = Vector3(2.001, 0, 0)
	assert are_sphere_and_aabb_colliding(sphere, aabb) is False
	
	
def test_aabb_collisions():
	aabb_a = AABBCollider(Vector3(0, 0, 0), Vector3(2, 2, 2))
	aabb_b = AABBCollider(Vector3(2, 0, 0), Vector3(2, 2, 2))
	
	assert are_aabb_colliding(aabb_a, aabb_b) is True
	
	aabb_b.center = Vector3(2.1, 0, 0)
	assert are_aabb_colliding(aabb_a, aabb_b) is False
