# encoding : UTF-8

from pygame import *
from math import tan, radians, floor
from settings import *


class Camera:
	"""
	Class who represents a 3D camera with some locked degrees of freedom.
	
	Camera object can move along each world axis (X, Y, Z) and rotate along Y axis.
	Rotation is automatically compute with self.position and self.focus_point, the 3D point to focus on in world
	coordinates. 'y' component of focused point is ignored for camera rotation but not for translation ; camera always
	points in a (XZ) direction.
	
	Camera object is defined by :
		- :var pygame.Vector3 self.position: 3D camera position in world coordinates
		- :var pygame.Vector3 self.focus_point: 3D point in which camera focus on
		- :var int self.w: pixel width of camera screen
		- :var int self.h: pixel height of camera screen
		- :var float self.fov_angle: angle in degrees of camera FOV
		- :var pygame.Surface self.surface: camera screen surface
		
	"""
	def __init__(self, display_manager, position, focus_point, w=800, h=640, fov_angle=60):
		"""
		Init object.
		
		:param DisplayManager display_manager: Display manager on which camera is attached
		:param pygame.Vector3 position: 3D position of camera in world coordinates
		:param pygame.Vector3 focus_point: 3D point in which camera focus on
		:param int w: pixel width of camera screen
		:param int h: pixel height of camera screen
		:param float fov_angle: angle in degrees of camera FOV
		"""
		self.display_manager = display_manager
		self.w = w
		self.h = h
		self._position = Vector3(position)
		self._focus_point = Vector3(focus_point)  # y component will be ignored
		
		self.fov_angle = fov_angle
		self._fov = tan(radians(self.fov_angle))
		self._w_vect = Vector3(1, 0, 0)
		
		self._process_w_vector()
		
		self.surface = Surface((self.w, self.h))
	
	@property  # a change of self.position may change self._w_vect
	def position(self):
		return self._position
	
	@position.setter
	def position(self, value):
		self._position = value
		self._process_w_vector()
	
	@property # a change of self.focus_point may change self._w_vect
	def focus_point(self):
		return self._focus_point
	
	@focus_point.setter
	def focus_point(self, value):
		self._focus_point = value
		self._position.y = value.y
		self._process_w_vector()
	
	def _process_w_vector(self):
		"""
		Process w vector, normalised vector in (camera position/focus point) direction.
		
		:return: None
		"""
		focus_pt = Vector3(self.focus_point)
		focus_pt.y = self.position.y
		self._w_vect = (self.position - focus_pt).normalize()
	
	def world_to_cam_3d_coords(self, w_pt):
		"""
		Return coordinates from a 3D point from world to camera referential.
		
		3D point in camera coordinates (xc, yc, zc) are defined as :
			- Origin (0, 0, 0) is self.position (C point in draft)  C---> Xc
			- Directions (Xc, Yc, Zc) are :                         |
				- Xc : left to right                                |   + M(xc, yc, zc)
				- Yc : up to bottom                                Yc
				- Zc : in front of camera to behind (a point with a negative zc value is in the camera field)

		:param pygame.Vector3 w_pt: 3D world point
		:return: w_pt in camera coordinates (xc, yc, zc)
		:rtype pygame.Vector3
		"""
		# translation
		t_pt = w_pt - self.position
		
		# rotation
		sin_a = self._w_vect[2]
		cos_a = self._w_vect[0]
		
		c_pt = Vector3(t_pt[1], sin_a * t_pt[0] - cos_a * t_pt[2], cos_a * t_pt[0] + sin_a * t_pt[2])
		
		return c_pt
		
	def world_to_pixel_coords(self, pt_3d):
		"""
		Return pixel coordinates from a 3D world point.
		
		From a 3D point in world coordinates, process and return pixel coordinates.
		Pixel coordinates/camera-screen emplacement :
			- (0, 0)        : top-left corner
			- (self.w, 0)   : top-right corner
			- (0, self.h)   : bottom-left corner
		
		:param pygame.Vector3 pt_3d: 3D world point
		:return: (u, v) camera-screen coordinates
		:rtype: tuple(int, int)
		"""
		u, v = 0, 0
		
		pt_3c = self.world_to_cam_3d_coords(pt_3d)
		
		if pt_3c[2] != 0:  # if point is distinct from camera center
			u = int(floor(-self.w / (2 * self._fov) * pt_3c[0] / pt_3c[2]) + self.w / 2)
			v = int(floor(-self.h / (2 * self._fov) * pt_3c[1] / pt_3c[2]) + self.h / 2)
		return u, v
	