# encoding : UTF-8

from pygame import *
import pytest

from Engine.Display import Camera


@pytest.fixture()
def horizontal_camera():
	return Camera(None, (5, 0, 0), (0, 0, 0), w=100, h=100, fov_angle=60)

@pytest.fixture()
def oblique_camera():
	return Camera(None, (3, 0, 4), (0, 0, 0), w=100, h=100, fov_angle=60)  # for 3 4 5 tri (rect tri)

@pytest.fixture()
def not_centered_camera():
	return Camera(None, (3+5, 0+5, 4+5), (0+5, 0+5, 0+5), w=100, h=100, fov_angle=60)


def test_world_to_cam_3d_coords(horizontal_camera, oblique_camera, not_centered_camera):
	center_pt = Vector3(0, 0, 0)
	assert horizontal_camera.world_to_cam_3d_coords(center_pt) == Vector3(0, 0, -5)
	assert oblique_camera.world_to_cam_3d_coords(center_pt) == Vector3(0, 0, -5)
	
	assert not_centered_camera.world_to_cam_3d_coords(not_centered_camera.focus_point) == Vector3(0, 0, -5)
	

def test_world_to_pixel_coords(horizontal_camera, oblique_camera, not_centered_camera):
	for cam in (horizontal_camera, oblique_camera, not_centered_camera):
		# center
		center_pt = Vector3(cam.focus_point)
		u, v = cam.world_to_pixel_coords(center_pt)
		assert u == cam.w / 2 or u == cam.w / 2 - 1  # -1 because of imprecision due to continuous/discrete conversion
		assert v == cam.h / 2 or v == cam.h / 2 - 1  # same thing
		
		# point in 4 screen areas (top-left, top-right, bottom-left and bottom-right)
		tl_pt = Vector3(0, -1, 1) + cam.focus_point
		tr_pt = Vector3(0, 1, 1) + cam.focus_point
		bl_pt = Vector3(0, -1, -1) + cam.focus_point
		br_pt = Vector3(0, 1, -1) + cam.focus_point
		
		# test if points are in correct area
		u, v = cam.world_to_pixel_coords(tl_pt)
		assert u < cam.w / 2 and v < cam.h / 2
		
		u, v = cam.world_to_pixel_coords(tr_pt)
		assert u > cam.w / 2 and v < cam.h / 2
		
		u, v = cam.world_to_pixel_coords(bl_pt)
		assert u < cam.w / 2 and v > cam.h / 2
		
		u, v = cam.world_to_pixel_coords(br_pt)
		assert u > cam.w / 2 and v > cam.h / 2
	