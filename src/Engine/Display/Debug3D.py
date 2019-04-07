# encoding : UTF-8

from pygame import *
from settings import *


def draw_sphere(camera, center, radius):
	# process r_px : radius in pixel
	c_pos = Vector3(center)
	if SIZE_INDEPENDENT_FROM_Y_POS:
		c_pos.y = camera.position.y
	if SIZE_INDEPENDENT_FROM_Z_POS:
		c_pos.z = camera.position.z
	r_px = int((Vector2(camera.world_to_pixel_coords(c_pos) -
	            Vector2(camera.world_to_pixel_coords(c_pos + radius * Vector3(0, 1, 0)))).magnitude()))

	draw.circle(camera.surface, DBG_COLOR_SPHERE, camera.world_to_pixel_coords(center), r_px)

def draw_horizontal_ellipse(camera, pos, r):
	# corners of shadow (trapeze)
	t_l = camera.world_to_pixel_coords(Vector3(pos) + (-r, -r, 0))
	t_r = camera.world_to_pixel_coords(Vector3(pos) + (-r, r, 0))
	b_l = camera.world_to_pixel_coords(Vector3(pos) + (r, -r, 0))
	b_r = camera.world_to_pixel_coords(Vector3(pos) + (r, r, 0))

	# approximate rect
	r_pos = [int(0.5 * (t_l[0] + b_l[0])), t_l[1]]
	r_w = int(0.5 * (t_r[0] + b_r[0]) - r_pos[0])
	r_h = b_r[1] - r_pos[1]
	if r_h < 0:
		r_pos[1] += r_h
		r_h = -r_h
	rect = Rect(r_pos, (r_w, r_h))

	draw.ellipse(camera.surface, DBG_COLOR_SHADOW, rect)
	draw.polygon(camera.surface, DBG_COLOR_SHADOW_TRAPEZE, [t_l, t_r, b_r, b_l], 1)


def draw_polygon(camera, pts):
	draw.polygon(camera.surface, DBG_COLOR_POLYGON, [(camera.world_to_pixel_coords(pt)) for pt in pts])

def draw_line(camera, ptA, ptB):
	draw.line(camera.surface, DBG_COLOR_LINE, camera.world_to_pixel_coords(ptA), camera.world_to_pixel_coords(ptB))

def draw_aligned_axis_box(camera, center, length_x, length_y, length_z):
	top_pts = [(center.x - length_x/2, center.y - length_y/2, center.z + length_z/2),
	           (center.x - length_x/2, center.y + length_y/2, center.z + length_z/2),
	           (center.x + length_x/2, center.y + length_y/2, center.z + length_z/2),
	           (center.x + length_x/2, center.y - length_y/2, center.z + length_z/2)]
	bottom_pts = [(center.x - length_x / 2, center.y - length_y / 2, center.z - length_z / 2),
	              (center.x - length_x / 2, center.y + length_y / 2, center.z - length_z / 2),
	              (center.x + length_x / 2, center.y + length_y / 2, center.z - length_z / 2),
	              (center.x + length_x / 2, center.y - length_y / 2, center.z - length_z / 2)]

	# to 2d coords
	top_pts = [(camera.world_to_pixel_coords(pt)) for pt in top_pts]
	bottom_pts = [(camera.world_to_pixel_coords(pt)) for pt in bottom_pts]

	draw.polygon(camera.surface, DBG_COLOR_AAB, top_pts, 1)                                 # top quad
	draw.polygon(camera.surface, DBG_COLOR_AAB, bottom_pts, 1)                              # bottom quad
	draw.polygon(camera.surface, DBG_COLOR_AAB, [*top_pts[:2], bottom_pts[1], bottom_pts[0]], 1)           # -x quad
	draw.polygon(camera.surface, DBG_COLOR_AAB, [*top_pts[2:], bottom_pts[3], bottom_pts[2]], 1)           # +x quad



