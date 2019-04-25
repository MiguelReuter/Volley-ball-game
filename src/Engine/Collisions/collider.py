# encoding : UTF-8

from pygame.math import *

from ..Display import Debug3D


class Collider:
	def __init__(self):
		pass
	
	def draw(self, display_manager):
		pass
	
	
class SphereCollider(Collider):
	def __init__(self, center, radius):
		super().__init__()
		self.center = center
		self.radius = radius
		
	def draw(self, display_manager):
		Debug3D.draw_sphere(display_manager, self.center, self.radius)
		
		
class AABBCollider(Collider):
	def __init__(self, center, size3):
		super().__init__()
		self.center = center
		self.size3 = size3
		
	def draw(self, display_manager):
		Debug3D.draw_aligned_axis_box(display_manager, self.center, *self.size3)
	

def are_spheres_colliding(sphere_a, sphere_b):
	"""
	Return True if spheres are colliding.
	
	:param SphereCollider sphere_a: sphere a collider
	:param SphereCollider sphere_b: sphere b collider
	:return: True if spheres are colliding
	:rtype bool:
	"""
	return (sphere_a.center - sphere_b.center).length_squared() <= (sphere_a.radius + sphere_b.radius)**2


def are_aabb_colliding(a, b):
	"""
	Return True if given AABB are colliding.
	
	:param AABBCollider a: AABB a
	:param AABBCollider b: AABB b
	:return: True if AABB are colliding
	:rtype bool:
	"""
	a_min = [a.center[i] - a.size3[i] / 2 for i in range(3)]
	a_max = [a.center[i] + a.size3[i] / 2 for i in range(3)]
	b_min = [b.center[i] - b.size3[i] / 2 for i in range(3)]
	b_max = [b.center[i] + b.size3[i] / 2 for i in range(3)]

	return (a_min[0] <= b_max[0] and a_max[0] >= b_min[0]) and \
	       (a_min[1] <= b_max[1] and a_max[1] >= b_min[1]) and \
	       (a_min[2] <= b_max[2] and a_max[2] >= b_min[2])


def are_sphere_and_aabb_colliding(sphere, aabb):
	"""
	Return True if given sphere and AABB are colliding.
	
	:param SphereCollider sphere: sphere collider
	:param AABBCollider aabb: AABB collider
	:return: True if sphere and AABB are colliding
	:rtype bool:
	"""
	
	# compute sq_dist, squared distance between sphere center and AABB
	sq_dist = 0.0
	for i in range(3):
		v = sphere.center[i]
		if v < aabb.center[i] - aabb.size3[i] / 2:
			sq_dist += (aabb.center[i] - aabb.size3[i] / 2 - v)**2
		if v > aabb.center[i] + aabb.size3[i] / 2:
			sq_dist += (aabb.center[i] + aabb.size3[i] / 2 - v)**2
	
	return sq_dist <= sphere.radius**2
