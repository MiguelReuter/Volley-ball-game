# encoding : UTF-8

from pygame import *
from math import sqrt
from settings import G


def find_initial_velocity(origin_pos, target_pos, wanted_center_height):
	"""
	Return initial velocity to apply on a ball to reach a target from an origin position and a specified height.
	
	Process initial velocity in world coordinates to apply on a ball. The specified height is taken in account for the
	ball trajectory. If target and origin y sign values are different, the wanted height will be on y = 0 (net
	position). Else, the wanted height will be on the middle of trajectory.
	
	
	:param pygame.Vector3 origin_pos: origin position, the point where the ball will be thrown from
	:param pygame.Vector3 target_pos: the desired target position the ball will reach
	:param float wanted_center_height: height desired on net place
	:return: velocity to apply to the ball
	:rtype pygame.Vector3:
	"""
	
	assert target_pos != origin_pos
	assert wanted_center_height > origin_pos.z
	assert wanted_center_height > target_pos.z
	
	# u vector : unit vector in XY plane from origin to target position
	u = Vector3(target_pos - origin_pos)
	u.z = 0
	u = u.normalize()
	
	# ut, zt : coordinates of target point in (u, z) ref
	TO = (target_pos - origin_pos)
	TO.z = 0
	
	ut = TO.length()
	zt = target_pos.z - origin_pos.z
	
	# uh, zh : coordinates of point above the net in (u, z) ref
	alpha = 0.5
	if origin_pos.y * target_pos.y < 0:  # if target and origin points are not in the same court side
		alpha = abs(origin_pos.y / (target_pos.y - origin_pos.y))
	uh = alpha * ut
	zh = wanted_center_height - origin_pos.z
	
	# process initial velocity to apply in (u, z) ref : vo_u, vo_z
	# not trivial equations, from math and physics resolutions
	a = (ut/uh * zh - zt)
	c = G * ut / 2 * (uh - ut)
	delta = -4 * a * c
	vo_u = sqrt(delta) / (2 * a)
	vo_z = zh * (vo_u / uh) + uh / vo_u * G / 2
	
	return Vector3(vo_u * u + Vector3(0, 0, vo_z))
