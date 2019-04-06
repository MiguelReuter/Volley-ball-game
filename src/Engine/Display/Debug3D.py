# encoding : UTF-8

from pygame import *
from settings import *


def draw_sphere(camera, center, radius):
	# TODO : r_px must be processed with a norm2 ?
	r_px = camera.world_to_pixel_coords(center + Vector3(0, radius, 0))[0] - camera.world_to_pixel_coords(center)[0]
	draw.circle(camera.surface, DBG_COLOR_SPHERE, camera.world_to_pixel_coords(center), r_px)

def draw_horizontal_ellipse(camera, pos, r):
	# TODO : draft, messy
	pts = [camera.world_to_pixel_coords(Vector3(pos) + (0, -r, 0)),
	       camera.world_to_pixel_coords(Vector3(pos) + (0, r, 0))]
	pts2 = [camera.world_to_pixel_coords(Vector3(pos) + (-r, 0, 0)),
	        camera.world_to_pixel_coords(Vector3(pos) + (r, 0, 0))]
	rect = Rect(pts[0], (abs(pts[1][0] - pts[0][0]), abs(pts2[1][1] - pts2[0][1])))
	draw.ellipse(camera.surface, DBG_COLOR_SHADOW, rect)
	draw.rect(camera.surface, (0, 255, 0), rect, 2)

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



