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


def draw_sphere(display_manager, center, radius, col=None):
	"""
	Draw a filled sphere on camera screen.
	
	:param DisplayManager display_manager: display manager used to draw
	:param pygame.Vector3 center: center of sphere
	:param float radius: radius (world scale, not in pixel) of sphere
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_SPHERE:
	:return: None
	"""
	if col is None:
		col = DBG_COLOR_SPHERE
	
	# process r_px : radius in pixel
	camera = display_manager.camera
	surface_size = display_manager.debug_surface.get_size()
	
	c_pos = Vector3(center)
	if SIZE_INDEPENDENT_FROM_Y_POS:
		c_pos.y = camera.position.y
	if SIZE_INDEPENDENT_FROM_Z_POS:
		c_pos.z = camera.position.z
	r_px = int((Vector2(camera.world_to_pixel_coords(c_pos, surface_size) -
	            Vector2(camera.world_to_pixel_coords(c_pos + radius * Vector3(0, 1, 0), surface_size))).magnitude()))

	draw.circle(display_manager.debug_surface, col,
	            camera.world_to_pixel_coords(center, surface_size), r_px)


def draw_horizontal_ellipse(display_manager, center, radius):
	"""
	Draw a filled ellipse and a unfilled bound trapeze in XY 3D plane on camera screen.
	
	:param DisplayManager display_manager: display manager used to draw
	:param pygame.Vector3 center: center of ellipse
	:param float radius: radius (world scale, not in pixel) of ellipse
	:return: None
	"""
	camera = display_manager.camera
	surface_size = display_manager.debug_surface.get_size()
	
	# corners of shadow (trapeze)
	t_l = camera.world_to_pixel_coords(Vector3(center) + (-radius, -radius, 0), surface_size)
	t_r = camera.world_to_pixel_coords(Vector3(center) + (-radius, radius, 0), surface_size)
	b_l = camera.world_to_pixel_coords(Vector3(center) + (radius, -radius, 0), surface_size)
	b_r = camera.world_to_pixel_coords(Vector3(center) + (radius, radius, 0), surface_size)
	
	# approximate rect
	r_pos = [int(0.5 * (t_l[0] + b_l[0])), t_l[1]]
	r_w = int(0.5 * (t_r[0] + b_r[0]) - r_pos[0])
	r_h = b_r[1] - r_pos[1]
	if r_h < 0:
		r_pos[1] += r_h
		r_h = -r_h
	rect = Rect(r_pos, (r_w, r_h))
	
	if r_w >= r_h:
		draw.ellipse(display_manager.debug_surface, DBG_COLOR_HOR_ELLIPSE, rect)
	draw.polygon(display_manager.debug_surface, DBG_COLOR_SHADOW_HOR_ELLIPSE_TRAPEZE, [t_l, t_r, b_r, b_l], 1)


def draw_polygon(display_manager, pts, col=None):
	"""
	Draw a closed 3D polygon on camera screen.
	
	:param DisplayManager display_manager: display manager used to draw
	:param list(pygame.Vector3) pts: 3D world points which define polygon
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_POLYGON:
	:return: None
	"""
	if col is None:
		col = DBG_COLOR_POLYGON
	camera = display_manager.camera
	surface_size = display_manager.debug_surface.get_size()
	
	draw.polygon(display_manager.debug_surface, col,
	             [(camera.world_to_pixel_coords(pt, surface_size)) for pt in pts])


def draw_line(display_manager, pt_a, pt_b, col=None):
	"""
	Draw a 3D line on camera screen.
	
	:param DisplayManager display_manager: display manager used to draw
	:param pygame.Vector3 pt_a: 3D point of line start
	:param pygame.Vector3 pt_b: 3D point of line end
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_LINE:
	:return: None
	"""
	if col is None:
		col = DBG_COLOR_LINE
	
	camera = display_manager.camera
	surface_size = display_manager.debug_surface.get_size()
	
	draw.line(display_manager.debug_surface, col,
	          camera.world_to_pixel_coords(pt_a, surface_size),
	          camera.world_to_pixel_coords(pt_b, surface_size))


def draw_aligned_axis_box(display_manager, center, length_x, length_y, length_z, col=None):
	"""
	Draw an 3D aligned-axis box on camera screen.
	
	Drawn box will be aligned to (X, Y, Z) world directions.
	
	:param DisplayManager display_manager: display manager used to draw
	:param pygame.Vector3 center: center of box
	:param float length_x: box length along x axis
	:param float length_y: box length along y axis
	:param float length_z: box length along z axis
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_AAB:
	:return: None
	"""
	if col is None:
		col = DBG_COLOR_AAB
	
	camera = display_manager.camera
	surface_size = display_manager.debug_surface.get_size()
	
	top_pts = [(center.x - length_x / 2, center.y - length_y / 2, center.z + length_z / 2),
	           (center.x - length_x / 2, center.y + length_y / 2, center.z + length_z / 2),
	           (center.x + length_x / 2, center.y + length_y / 2, center.z + length_z / 2),
	           (center.x + length_x / 2, center.y - length_y / 2, center.z + length_z / 2)]
	bottom_pts = [(center.x - length_x / 2, center.y - length_y / 2, center.z - length_z / 2),
	              (center.x - length_x / 2, center.y + length_y / 2, center.z - length_z / 2),
	              (center.x + length_x / 2, center.y + length_y / 2, center.z - length_z / 2),
	              (center.x + length_x / 2, center.y - length_y / 2, center.z - length_z / 2)]
	
	# to 2d coords
	top_pts = [(camera.world_to_pixel_coords(pt, surface_size)) for pt in top_pts]
	bottom_pts = [(camera.world_to_pixel_coords(pt, surface_size)) for pt in bottom_pts]
	
	draw.polygon(display_manager.debug_surface, col, top_pts, 1)  # top quad
	draw.polygon(display_manager.debug_surface, col, bottom_pts, 1)  # bottom quad
	draw.polygon(display_manager.debug_surface, col, [*top_pts[:2], bottom_pts[1], bottom_pts[0]], 1)  # -x quad
	draw.polygon(display_manager.debug_surface, col, [*top_pts[2:], bottom_pts[3], bottom_pts[2]], 1)  # +x quad
