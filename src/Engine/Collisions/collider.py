# encoding : UTF-8

from pygame import Vector3
from Engine.Display import debug3D_utils


class Collider:
	def __init__(self):
		pass
	
	def draw(self):
		pass
	
	
class SphereCollider(Collider):
	def __init__(self, center, radius):
		super().__init__()
		self.center = center
		self.radius = radius
		
	def draw(self):
		return debug3D_utils.draw_sphere(self.center, self.radius)
		
		
class AABBCollider(Collider):
	def __init__(self, center, size3):
		super().__init__()
		self.center = center
		self.size3 = size3
		
	def draw(self):
		return debug3D_utils.draw_aligned_axis_box(self.center, *self.size3)
	

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


def are_sphere_and_finite_plane_colliding(sphere, aabb, previous_sphere_position):
	"""
	Return True if given sphere and plane are colliding.
	
	Given AABB collider is supposed to have y size equals to 0 (for finite plane).
	If there is a collision, collision point and ball position at collision moment are returned too.
	:param SphereCollider sphere: sphere collider
	:param AABBCollider aabb: AABB collider, size along y axis is supposed to be 0
	:param pygame.Vector3 previous_sphere_position: previous position of ball
	:return: True if sphere and AABB are colliding, collision point and ball position at collision moment if there is a
	collision
	:rtype (True, Vector3, Vector3)
	    or (False, None, None)          according to first bool:
	"""
	if are_sphere_and_aabb_colliding(sphere, aabb):
		x_min = aabb.center.x - aabb.size3[0] / 2
		x_max = aabb.center.x + aabb.size3[0] / 2
		y = aabb.center.y
		z_min = aabb.center.z - aabb.size3[2] / 2
		z_max = aabb.center.z + aabb.size3[2] / 2
		
		# find collision point
		
		# center of net
		if (x_min <= sphere.center.x <= x_max) & (z_min <= sphere.center.z <= z_max):
			collision_point = Vector3(sphere.center.x, y, sphere.center.z)
		elif (x_min <= sphere.center.x <= x_max):
			# top
			if (Vector3(0, sphere.center.y - y, sphere.center.z - z_max).length_squared() <= sphere.radius ** 2):
				collision_point = Vector3(sphere.center.x, y, z_max)
			# bottom
			elif (Vector3(0, sphere.center.y - y, sphere.center.z - z_min).length_squared() <= sphere.radius ** 2):
				collision_point = Vector3(sphere.center.x, y, z_min)
		elif (z_min <= sphere.center.z <= z_max):
			# left
			if (Vector3(sphere.center.x - x_max, sphere.center.y - y, 0).length_squared() <= sphere.radius ** 2):
				collision_point = Vector3(x_max, y, sphere.center.z)
			# right
			elif (Vector3(sphere.center.x - x_min, sphere.center.y - y, 0).length_squared() <= sphere.radius ** 2):
				collision_point = Vector3(x_min, y, sphere.center.z)
		# corners of net
		elif (Vector3(x_min, y, z_min) - sphere.center).length_squared() <= sphere.radius ** 2:
			collision_point = Vector3(x_min, y, z_min)
		elif (Vector3(x_min, y, z_max) - sphere.center).length_squared() <= sphere.radius ** 2:
			collision_point = Vector3(x_min, y, z_max)
		elif (Vector3(x_max, y, z_min) - sphere.center).length_squared() <= sphere.radius ** 2:
			collision_point = Vector3(x_max, y, z_min)
		elif (Vector3(x_max, y, z_max) - sphere.center).length_squared() <= sphere.radius ** 2:
			collision_point = Vector3(x_max, y, z_max)
		# there's a collision but collision point not found !
		else:
			assert -1
			
		# u vect
		u_vect = Vector3(collision_point - previous_sphere_position).normalize()
		ball_pos_at_collision = -sphere.radius * u_vect + collision_point
		
		return True, collision_point, ball_pos_at_collision
	return False, None, None
	
