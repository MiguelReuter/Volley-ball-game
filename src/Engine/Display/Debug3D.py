# encoding : UTF-8

from pygame import *

# flags
SIZE_INDEPENDENT_FROM_Y_POS = True
SIZE_INDEPENDENT_FROM_Z_POS = False

# colors
DBG_COLOR_LINE = (100, 100, 255)
DBG_COLOR_SPHERE = (200, 0, 0)
DBG_COLOR_POLYGON = (200, 200, 200)
DBG_COLOR_AAB = (0, 200, 200)
DBG_COLOR_HOR_ELLIPSE = (20, 20, 20)
DBG_COLOR_SHADOW_HOR_ELLIPSE_TRAPEZE = (255, 0, 255)


def draw_sphere(camera, center, radius):
	"""
	Draw a filled sphere on camera screen.
	
	:param Camera camera: camera on which sphere will be drawn
	:param pygame.Vector3 center: center of sphere
	:param float radius: radius (world scale, not in pixel) of sphere
	:return: None
	"""
	# process r_px : radius in pixel
	c_pos = Vector3(center)
	if SIZE_INDEPENDENT_FROM_Y_POS:
		c_pos.y = camera.position.y
	if SIZE_INDEPENDENT_FROM_Z_POS:
		c_pos.z = camera.position.z
	r_px = int((Vector2(camera.world_to_pixel_coords(c_pos) -
	            Vector2(camera.world_to_pixel_coords(c_pos + radius * Vector3(0, 1, 0)))).magnitude()))

	draw.circle(camera.surface, DBG_COLOR_SPHERE, camera.world_to_pixel_coords(center), r_px)


def draw_horizontal_ellipse(camera, center, radius):
	"""
	Draw a filled ellipse and a unfilled bound trapeze in XY 3D plane on camera screen.
	
	:param Camera camera: camera on which ellipse will be drawn
	:param pygame.Vector3 center: center of ellipse
	:param float radius: radius (world scale, not in pixel) of ellipse
	:return: None
	"""
	# corners of shadow (trapeze)
	t_l = camera.world_to_pixel_coords(Vector3(center) + (-radius, -radius, 0))
	t_r = camera.world_to_pixel_coords(Vector3(center) + (-radius, radius, 0))
	b_l = camera.world_to_pixel_coords(Vector3(center) + (radius, -radius, 0))
	b_r = camera.world_to_pixel_coords(Vector3(center) + (radius, radius, 0))

	# approximate rect
	r_pos = [int(0.5 * (t_l[0] + b_l[0])), t_l[1]]
	r_w = int(0.5 * (t_r[0] + b_r[0]) - r_pos[0])
	r_h = b_r[1] - r_pos[1]
	if r_h < 0:
		r_pos[1] += r_h
		r_h = -r_h
	rect = Rect(r_pos, (r_w, r_h))

	draw.ellipse(camera.surface, DBG_COLOR_HOR_ELLIPSE, rect)
	draw.polygon(camera.surface, DBG_COLOR_SHADOW_HOR_ELLIPSE_TRAPEZE, [t_l, t_r, b_r, b_l], 1)


def draw_polygon(camera, pts):
	"""
	Draw a closed 3D polygon on camera screen.
	
	:param Camera camera: camera on which polygon will be drawn
	:param list(pygame.Vector3) pts: 3D world points which define polygon
	:return: None
	"""
	draw.polygon(camera.surface, DBG_COLOR_POLYGON, [(camera.world_to_pixel_coords(pt)) for pt in pts])


def draw_line(camera, ptA, ptB):
	"""
	Draw a 3D line on camera screen.
	
	:param Camera camera: camera on which line will be drawn
	:param pygame.Vector3 ptA: 3D point of line start
	:param pygame.Vector3 ptB: 3D point of line end
	:return: None
	"""
	draw.line(camera.surface, DBG_COLOR_LINE, camera.world_to_pixel_coords(ptA), camera.world_to_pixel_coords(ptB))


def draw_aligned_axis_box(camera, center, length_x, length_y, length_z):
	"""
	Draw an 3D aligned-axis box on camera screen.
	
	Drawn box will be aligned to (X, Y, Z) world directions.
	
	:param Camera camera: camera on which box will be drawn
	:param pygame.Vector3 center: center of box
	:param float length_x: box length along x axis
	:param float length_y: box length along y axis
	:param float length_z: box length along z axis
	:return: None
	"""
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
