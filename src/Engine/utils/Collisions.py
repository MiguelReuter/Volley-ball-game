# encoding : UTF-8

from pygame.math import *


def are_spheres_colliding(center_1, radius_1, center_2, radius_2):
	"""
	Return True if spheres are colliding.
	
	:param pygame.math.Vector3 center_1: center of sphere 1 in world coordinates
	:param float radius_1: radius of sphere 1
	:param pygame.math.Vector3 center_2: center of sphere 2 in world coordinates
	:param float radius_2: radius of sphere 2
	:return: True if spheres are colliding
	:rtype bool:
	"""
	return (center_2 - center_1).length_squared() <= (radius_1 + radius_2)**2


def are_AABB_colliding(center_a, size3_a, center_b, size3_b):
	"""
	Return True if given AABB are colliding.
	
	:param pygame.math.Vector3 center_a: center of aabb a
	:param pygame.math.Vector3 size3_a: aabb a size for each dimensions
	:param pygame.math.Vector3 center_b: center of aabb b
	:param pygame.math.Vector3 size3_b: aabb b size for each dimensions
	:return: True if AABB are colliding
	:rtype bool:
	"""
	a_min = [center_a[i] - size3_a[i] / 2 for i in range(3)]
	a_max = [center_a[i] + size3_a[i] / 2 for i in range(3)]
	b_min = [center_b[i] - size3_b[i] / 2 for i in range(3)]
	b_max = [center_b[i] + size3_b[i] / 2 for i in range(3)]

	return (a_min[0] <= b_max[0] and a_max[0] >= b_min[0]) and \
	       (a_min[1] <= b_max[1] and a_max[1] >= b_min[1]) and \
	       (a_min[2] <= b_max[2] and a_max[2] >= b_min[2])


def are_sphere_and_AABB_colliding(sphere_center, sphere_radius, aabb_center, aabb_size3):
	"""
	Return True if given sphere and AABB are colliding.
	
	:param pygame.math.Vector3 sphere_center: sphere center
	:param sphere_radius: sphere radius
	:param pygame.math.Vector3 aabb_center: aabb center
	:param pygame.math.Vector3 aabb_size3: aabb size for each dimensions
	:return: True if sphere and AABB are colliding
	:rtype bool:
	"""
	
	# compute sq_dist, squared distance between sphere center and AABB
	sq_dist = 0.0
	for i in range(3):
		v = sphere_center[i]
		if v < aabb_center[i] - aabb_size3[i] / 2:
			sq_dist += (aabb_center[i] - aabb_size3[i] / 2 - v)**2
		if v > aabb_center[i] + aabb_size3[i] / 2:
			sq_dist += (aabb_center[i] + aabb_size3[i] / 2 - v)**2
	
	return sq_dist <= sphere_radius**2
