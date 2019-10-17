# encoding : UTF-8

from pygame import Vector3
from math import sqrt
from Settings import G


def find_initial_velocity(origin_pos, target_pos, wanted_height):
	"""
	Return initial velocity to apply to a ball to reach a target from an origin position and a specified height.
	
	Process initial velocity in world coordinates to apply on a ball. The specified height is taken in account for the
	ball trajectory. If target and origin y sign values are different, the wanted height will be on y = 0 (net
	position). Else, the wanted height will be on the middle of trajectory, or at apogee trajectory during a
	vertical throw.
	
	:param pygame.Vector3 origin_pos: origin position, the point where the ball will be thrown from
	:param pygame.Vector3 target_pos: the desired target position the ball will reach
	:param float wanted_height: height desired on net place, middle of trajectory or at apogee
	:return: velocity to apply to the ball
	:rtype pygame.Vector3:
	"""
	assert wanted_height > origin_pos.z
	assert wanted_height > target_pos.z
	
	if target_pos.x == origin_pos.x and target_pos.y == origin_pos.y:  # vertical throw
		zh = wanted_height - origin_pos.z
		vo_z = sqrt(2 * G * zh)
		return Vector3(0, 0, vo_z)
	else:
		# u vector : unit vector in XY plane from origin to target position
		u = Vector3(target_pos - origin_pos)
		u.z = 0
		u = u.normalize()
		
		# ut, zt : coordinates of target point in (u, z) ref
		to_vect = (target_pos - origin_pos)
		to_vect.z = 0
		
		ut = to_vect.length()
		zt = target_pos.z - origin_pos.z
		
		# uh, zh : coordinates of point above the net in (u, z) ref
		alpha = 0.5
		if origin_pos.y * target_pos.y < 0:  # if target and origin points are not in the same court side
			alpha = abs(origin_pos.y / (target_pos.y - origin_pos.y))
		uh = alpha * ut
		zh = wanted_height - origin_pos.z
		
		# process initial velocity to apply in (u, z) ref : vo_u, vo_z
		# not trivial equations, from math and physics resolutions
		a = (ut/uh * zh - zt)
		c = G * ut / 2 * (uh - ut)
		delta = -4 * a * c
		vo_u = sqrt(delta) / (2 * a)
		vo_z = zh * (vo_u / uh) + uh / vo_u * G / 2
		
		return Vector3(vo_u * u + Vector3(0, 0, vo_z))


def find_target_position(origin_pos, initial_velocity, wanted_z=0):
	"""
	Find and return target ball position with a specified initial velocity and position.
	
	:param pygame.Vector3 origin_pos: initial ball position in world coordinates
	:param pygame.Vector3 initial_velocity: initial ball velocity in world coordinates
	:param float wanted_z: specify at which z value target position will be found
	:return: target ball position
	:rtype pygame.Vector3:
	"""
	# z_t
	z_t = wanted_z - origin_pos.z
	
	# u vector : unit vector in XY plane from origin to target position
	u = Vector3(initial_velocity)
	u.z = 0
	u = u.normalize() if u.length_squared() != 0 else Vector3()
	
	# get final time t_t
	t_t = get_time_at_z(initial_velocity.z, origin_pos.z, wanted_z)

	# u_t
	u_t = t_t * initial_velocity.dot(u)
	
	return u_t * u + origin_pos + Vector3(0, 0, z_t)


def get_time_polynomial_fun(vz_0, z_0, z_t):
	"""
	Get polynomial coefficients and delta value for time equation.

	Form of polynomial function is :
		a * t**2 + b * t + c = 0
	with t = 0 --> initial position

	:param float vz_0: initial vertical velocity ( > 0 for ascending)
	:param float z_0: initial z value
	:param float z_t: target z value
	:return: a, b, c and delta
	:rtype tuple(float):
	"""
	a = G / 2
	b = -vz_0
	c = z_t - z_0
	delta = b ** 2 - 4 * a * c

	return a, b, c, delta


def get_time_at_z(vz_0, z_0, z):
	"""
	Get time at specific height for a trajectory descending phase.

	:param float vz_0: initial vertical velocity ( > 0 for ascending)
	:param float z_0: initial z value
	:param float z: target z value
	:return: time in sec which when z is reached
	:rtype float:
	"""
	a, b, c, delta = get_time_polynomial_fun(vz_0, z_0, z)

	assert delta > 0
	return (-b + sqrt(delta)) / (2 * a)


def get_time_at_y(vy_0, y_0, y):
	"""
	Get time at specific y coordinate.

	:param float vy_0: initial velocity along y axis
	:param float y_0: initial y value
	:param float y: y value at which time is given
	:return: time in sec when y coordinate will be reached, or None if there is no solution
	:rtype: float or None
	"""
	delta_y = y - y_0
	if vy_0 != 0:
		return delta_y / vy_0
	return None


def get_z_at_y(initial_velocity, initial_position, z_t, y):
	a, b, c, _ = get_time_polynomial_fun(initial_velocity.z, initial_position.z, z_t)

	if initial_velocity.y != 0:
		t_y = (y - initial_position.y) / initial_velocity.y
		z_at_y = -(a * t_y**2 + b * t_y) + initial_position.z
		return z_at_y


def get_x_at_y(origin_pos, initial_velocity, y):
	dy = y - origin_pos.y

	if initial_velocity.y != 0:
		dt = dy / initial_velocity.y
		dx = dt * initial_velocity.x
		return origin_pos.x + dx
	else:
		return None


def _are_points_in_same_y_side(p1, p2):
	"""
	Return True if the 2 given points are on same side (y axis).
	
	usage examples :
		>>> p1 = Vector3(0, -5, 0)
		>>> p2 = Vector3(0, 10, 0)
		>>> _are_points_in_same_y_side(p1, p2)
		True
		>>> p3 = Vector3(20, -5, 0)
		>>> _are_points_in_same_y_side(p1, p3)
		False
	
	:param pygame.Vector3 p1: 1st point
	:param pygame.Vector3 p2: 2nd point
	:return: True if points are in same side
	"""
	return p1.y * p2.y < 0


def _apply_signed_threshold(value, min_thr=None, max_thr=None):
	"""
	Apply threshold on signed value.
	
	usage examples :
		>>> _apply_signed_threshold(0.678, min_thr=0.5)
		0.5
		>>> _apply_signed_threshold(-0.678, min_thr=0.5)
		-0.5
		>>> _apply_signed_threshold(0.678, max_thr=2.0)
		0.678
		>>> _apply_signed_threshold(20.678, max_thr=2.0)
		2.0
		>>> _apply_signed_threshold(-20, max_thr=2.0)
		-2.0
	
	:param float value: value to threshold
	:param float min_thr: nearest threshold from 0
	:param float max_thr: farthest threshold from 0
	:return: thresholded value
	:rtype float:
	"""
	sat_val = value
	
	if min_thr is not None:
		if sat_val < 0:
			sat_val = max(sat_val, -min_thr)
		else:
			sat_val = min(sat_val, min_thr)
	if max_thr is not None:
		if sat_val < 0:
			sat_val = max(sat_val, -max_thr)
		else:
			sat_val = min(sat_val, max_thr)
			
	return sat_val
