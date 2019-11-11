# encoding : UTF-8

from pygame import Vector2, Vector3, draw, Rect
from Engine.Display import DisplayManager


# flags
Y_DEPENDENT_SIZE = False
Z_DEPENDENT_SIZE = True

# colors
DBG_COLOR_LINE = (100, 100, 255)
DBG_COLOR_SPHERE = (200, 0, 0)
DBG_COLOR_POLYGON = (200, 200, 200)
DBG_COLOR_AAB = (0, 200, 200)
DBG_COLOR_HOR_ELLIPSE = (20, 20, 20)
DBG_COLOR_SHADOW_HOR_ELLIPSE_TRAPEZE = (255, 0, 255)


def draw_sphere(center, radius, col=None, width=0):
	"""
	Draw a sphere on camera screen.

	width in kwargs could be specified.

	:param pygame.Vector3 center: center of sphere
	:param float radius: radius (world scale, not in pixel) of sphere
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_SPHERE:
	:param int width: width of drawn sphere
	:return: rect bounding the changed pixels
	:rtype: pygame.Rect
	"""
	display_manager = DisplayManager.get_instance()
	if col is None:
		col = DBG_COLOR_SPHERE

	# process r_px : radius in pixel
	camera = display_manager.camera
	surface = display_manager.debug_3d.image
	surface_size = surface.get_size()

	r_px = camera.get_length_in_pixels_at(center, radius, surface_size, Y_DEPENDENT_SIZE, Z_DEPENDENT_SIZE)

	# prevent to have width greater than radius in pygame.draw.circle
	if width > r_px:
		width = 0
	# draw circle
	bounding_rect = draw.circle(surface, col, camera.world_to_pixel_coords(center, surface_size), r_px, width)

	# inflate rect (with width > 1, circle is drawn out of bounds else)
	if width != 0:
		bounding_rect.inflate_ip(2 * width, 2 * width)

	return bounding_rect


def draw_horizontal_ellipse(center, radius):
	"""
	Draw a filled ellipse and a unfilled bound trapeze in XY 3D plane on camera screen.
	
	:param pygame.Vector3 center: center of ellipse
	:param float radius: radius (world scale, not in pixel) of ellipse
	:return: rect bounding the changed pixels
	:rtype pygame.Rect:
	"""
	display_manager = DisplayManager.get_instance()
	camera = display_manager.camera
	surface = display_manager.debug_3d.image
	surface_size = surface.get_size()
	
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
		draw.ellipse(surface, DBG_COLOR_HOR_ELLIPSE, rect)
		
	# ellipse is in polygon rect, not need to return both rects
	return draw.polygon(surface, DBG_COLOR_SHADOW_HOR_ELLIPSE_TRAPEZE, [t_l, t_r, b_r, b_l], 1)


def draw_polygon(pts, col=None):
	"""
	Draw a closed 3D polygon on camera screen.
	
	:param list(pygame.Vector3) pts: 3D world points which define polygon
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_POLYGON:
	:return: rect bounding the changed pixels
	:rtype pygame.Rect:
	"""
	if col is None:
		col = DBG_COLOR_POLYGON

	display_manager = DisplayManager.get_instance()
	camera = display_manager.camera
	surface = display_manager.debug_3d.image
	surface_size = surface.get_size()
	
	return draw.polygon(surface, col, [(camera.world_to_pixel_coords(pt, surface_size)) for pt in pts])


def draw_line(pt_a, pt_b, col=None):
	"""
	Draw a 3D line on camera screen.
	
	:param pygame.Vector3 pt_a: 3D point of line start
	:param pygame.Vector3 pt_b: 3D point of line end
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_LINE:
	:return: rect bounding the changed pixels
	:rtype pygame.Rect:
	"""
	if col is None:
		col = DBG_COLOR_LINE

	display_manager = DisplayManager.get_instance()
	camera = display_manager.camera
	surface = display_manager.debug_3d.image
	surface_size = surface.get_size()
	
	return draw.line(surface, col, camera.world_to_pixel_coords(pt_a, surface_size),
	                               camera.world_to_pixel_coords(pt_b, surface_size))


def draw_aligned_axis_box(center, length_x, length_y, length_z, col=None):
	"""
	Draw an 3D aligned-axis box on camera screen.
	
	Drawn box will be aligned to (X, Y, Z) world directions.
	
	:param pygame.Vector3 center: center of box
	:param float length_x: box length along x axis
	:param float length_y: box length along y axis
	:param float length_z: box length along z axis
	:param tuple(int, int, int) col: drawing color. default is :var DBG_COLOR_AAB:
	:return: rect bounding the changed pixels
	:rtype pygame.Rect:
	"""
	if col is None:
		col = DBG_COLOR_AAB

	display_manager = DisplayManager.get_instance()
	camera = display_manager.camera
	surface = display_manager.debug_3d.image
	surface_size = surface.get_size()
	
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
	
	r_top = draw.polygon(surface, col, top_pts, 1)  # top quad
	r_bottom = draw.polygon(surface, col, bottom_pts, 1)  # bottom quad
	r_left = draw.polygon(surface, col, [*top_pts[:2], bottom_pts[1], bottom_pts[0]], 1)  # -x quad
	r_right = draw.polygon(surface, col, [*top_pts[2:], bottom_pts[3], bottom_pts[2]], 1)  # +x quad
	
	return r_top.unionall([r_bottom, r_left, r_right])
