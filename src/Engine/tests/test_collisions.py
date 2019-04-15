from pygame import *

from Engine.utils import Collisions


def test_spheres_collisions():
	sphere_a = Collisions.SphereCollider(Vector3(0, 0, 0), 1)
	sphere_b = Collisions.SphereCollider(Vector3(2, 0, 0), 1)

	assert Collisions.are_spheres_colliding(sphere_a, sphere_b) is True
	
	sphere_b.center = Vector3(2.001, 0, 0)
	assert Collisions.are_spheres_colliding(sphere_a, sphere_b) is False
	
	sphere_b.center = Vector3(2, 0, 0)
	sphere_b.radius = 0.5
	assert Collisions.are_spheres_colliding(sphere_a, sphere_b) is False


def test_sphere_and_aabb_collisions():
	sphere = Collisions.SphereCollider(Vector3(0, 0, 0), 1)
	aabb = Collisions.AABBCollider(Vector3(2, 0, 0), Vector3(2, 2, 2))
	
	assert Collisions.are_sphere_and_AABB_colliding(sphere, aabb) is True
	
	aabb.center = Vector3(2.001, 0, 0)
	assert Collisions.are_sphere_and_AABB_colliding(sphere, aabb) is False
	
	
def test_aabb_collisions():
	aabb_a = Collisions.AABBCollider(Vector3(0, 0, 0), Vector3(2, 2, 2))
	aabb_b = Collisions.AABBCollider(Vector3(2, 0, 0), Vector3(2, 2, 2))
	
	assert Collisions.are_AABB_colliding(aabb_a, aabb_b) is True
	
	aabb_b.center = Vector3(2.1, 0, 0)
	assert Collisions.are_AABB_colliding(aabb_a, aabb_b) is False
