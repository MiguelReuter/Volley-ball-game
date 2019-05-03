# encoding : UTF-8

from pygame import *
from math import sqrt
from Settings import G


THR_NEAR_ZONE = 2


def find_initial_velocity(origin_pos, target_pos, wanted_height):
	"""
	Return initial velocity to apply to a ball to reach a target from an origin position and a specified height.
	
	Process initial velocity in world coordinates to apply on a ball. The specified height is taken in account for the
	ball trajectory. If target and origin y sign values are different, the wanted height will be on y = 0 (net
	position). Else, the wanted height will be on the middle of trajectory.
	
	:param pygame.Vector3 origin_pos: origin position, the point where the ball will be thrown from
	:param pygame.Vector3 target_pos: the desired target position the ball will reach
	:param float wanted_height: height desired on net place
	:return: velocity to apply to the ball
	:rtype pygame.Vector3:
	"""
	assert target_pos != origin_pos
	assert wanted_height > origin_pos.z
	assert wanted_height > target_pos.z
	
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
	
	# find t_t : final time
	a = G / 2
	b = -initial_velocity.z
	c = z_t
	
	delta = b**2 - 4 * a * c
	assert delta > 0
	t_t = (-b + sqrt(delta)) / (2 * a)
	
	# u_t
	u_t = t_t * initial_velocity.dot(u)
	
	return u_t * u + origin_pos + Vector3(0, 0, z_t)
	

def get_n_points_in_trajectory(n, origin_pos, initial_velocity, wanted_z=0):
	"""
	Return n points in ball trajectory defined by origin position and initial velocity.
	
	:param int n: points count
	:param pygame.Vector3 origin_pos: initial ball position
	:param pygame.Vector3 initial_velocity: initial ball velocity
	:param float wanted_z: wanted height for final point (end of trajectory)
	:return: n points in list
	:rtype list(Vector3):
	"""
	# z_t
	z_t = wanted_z - origin_pos.z
	
	# u vector : unit vector in XY plane from origin to target position
	u = Vector3(initial_velocity)
	u.z = 0
	u = u.normalize()
	
	# find t_t : final time
	a = G / 2
	b = -initial_velocity.z
	c = z_t
	
	delta = b ** 2 - 4 * a * c
	assert delta > 0
	t_t = (-b + sqrt(delta)) / (2 * a)
	
	assert n > 1
	dt = t_t / (n - 1)
	pts = []
	for i in range(n):
		t_i = i * dt
		u_i = t_i * initial_velocity.dot(u)
		z_i = -t_i**2 / 2 * G + t_i * initial_velocity.z
		pts.append(Vector3(u_i * u + origin_pos + Vector3(0, 0, z_i)))
		
	return pts


def find_effective_target_position(origin_pos, target_pos, wanted_height):
	# TODO : /!\ method not used yet /!\
	# all targets and wanted heights are not physically possible for the player : huge velocity needed, skills...
	
	# TODO : add dependence on target and origin position
	eff_target_pos = Vector3(target_pos)
	eff_wanted_height = wanted_height
	if _are_points_in_same_y_side(origin_pos, target_pos):
		if abs(origin_pos.y) < THR_NEAR_ZONE:
			eff_target_pos.y = _apply_signed_threshold(eff_target_pos.y, min=THR_NEAR_ZONE)
			
	# TODO : add dependence on player direction and distance from the ball

	
	return eff_target_pos, eff_wanted_height


def _are_points_in_same_y_side(p1, p2):
	return p1.y * p2.y < 0


def _apply_signed_threshold(value, min_thr=None, max_thr=None):
	sat_val = value
	
	if min_thr is not None:
		if sat_val < 0:
			sat_val = max(sat_val, -min_thr)
		else:
			sat_val = min(sat_val, min_thr)
	if max_thr is not None:
		if sat_val < 0:
			sat_val = min(sat_val, -max_thr)
		else:
			sat_val = max(sat_val, max_thr)
			
	return sat_val
