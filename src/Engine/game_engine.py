# encoding : UTF-8

from Engine.Graphics.graphics_engine import *
from settings import *


import pygame as pg


def draw_court(camera, w, h, net_h):
	# TODO : refactor and move this function
	camera.draw_polygon([(-h / 2, -w / 2, 0), (-h / 2, w / 2, 0), (h / 2, w / 2, 0), (h / 2, -w / 2, 0)])
	
	# corners
	camera.draw_lines((-h / 2, -w / 2, 0), (-h / 2, -w / 2, 2))
	camera.draw_lines((-h / 2, w / 2, 0), (-h / 2, w / 2, 2))
	camera.draw_lines((h / 2, w / 2, 0), (h / 2, w / 2, 2))
	camera.draw_lines((h / 2, -w / 2, 0), (h / 2, -w / 2, 2))
	
	# net
	camera.draw_lines((-h / 2, 0, 0), (-h / 2, 0, net_h))
	camera.draw_lines((h / 2, 0, 0), (h / 2, 0, net_h))
	camera.draw_lines((-h / 2, 0, net_h), (h / 2, 0, net_h))
	camera.draw_lines((-h / 2, 0, net_h - 1), (h / 2, 0, net_h - 1))
	
	
class GameEngine:
	# TODO : singleton
	def __init__(self):
		self.graphics_engine = GraphicsEngine(self)
		self._create()
		
		self.ball_pos = pg.Vector3(0, 0, 2)
	
	def _create(self):
		self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		pg.display.set_caption(CAPTION)
	
	def run(self):
		quit_game = False
		while not quit_game:
			cam = self.graphics_engine.camera
			ball_position = self.ball_pos
			
			self.screen.blit(cam.surface, (0, 0))
			
			# draw basic polygon on the ground
			cam.surface.fill((0, 0, 0))
			draw_court(cam, 10, 6, 3)
			
			cam.draw_horizontal_ellipse((ball_position[0], ball_position[1], 0), 0.5)
			cam.draw_sphere(ball_position, 0.5)
			
			cam.draw_sphere((ball_position[0], ball_position[1], 0), 0.1)
			# cam.draw_horizontal_ellipse(ball_position, 0.5)
			
			# update keyboard events
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit_game = True
				if event.type == pg.KEYDOWN:
					# move camera
					if event.key == pg.K_UP:
						cam.position += (0, 0, 0.1)
					if event.key == pg.K_DOWN:
						cam.position += (0, 0, -0.1)
					if event.key == pg.K_LEFT:
						cam.position += (0, -0.1, 0)
					if event.key == pg.K_RIGHT:
						cam.position += (0, 0.1, 0)
					# move ball
					if event.key == pg.K_i:
						ball_position -= (0.1, 0, 0)
					if event.key == pg.K_j:
						ball_position -= (0, 0.1, 0)
					if event.key == pg.K_k:
						ball_position += (0.1, 0, 0)
					if event.key == pg.K_l:
						ball_position += (0, 0.1, 0)
					# quit
					if event.key in (pg.K_q, pg.K_ESCAPE):
						quit_game = True
				
				if event.type == pg.KEYUP:
					# debug
					if event.key == pg.K_SPACE:
						print("ball pos :", ball_position)
			
			# update screen
			pg.display.flip()