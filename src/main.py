# encoding : UTF8

import pygame
import src.Engine.Graphics.camera as camera

if __name__ == "__main__":
	pygame.init()
	pygame.key.set_repeat(10)
	screen = pygame.display.set_mode((800, 640))
	
	cam = camera.Camera((4, 0, 2), (0, 0, 2), fov_angle=60)
	
	quit_game = False

	ball_position = pygame.Vector3(0, 0, 2)

	cam.draw_horizontal_ellipse((0, -5, 0), 1)
	cam.draw_horizontal_ellipse((0, 5, 0), 1)


	while not quit_game:
		# clean screen
		#screen.fill((0, 0, 0))
		
		screen.blit(cam.surface, (0, 0))
		
		# draw basic polygon on the ground
		cam.surface.fill((0, 0, 0))
		cam.draw_polygon([(-2, -5, 0), (-2, 5, 0), (2, 5, 0), (2, -5, 0)])
		cam.draw_horizontal_ellipse((ball_position[0], ball_position[1], 0), 0.5)
		cam.draw_sphere(ball_position, 0.5)
		
		cam.draw_sphere((ball_position[0], ball_position[1], 0), 0.5)
		#cam.draw_horizontal_ellipse(ball_position, 0.5)

		# update keyboard events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game = True
			if event.type == pygame.KEYDOWN:
				# move camera
				if event.key == pygame.K_UP:
					cam.position += (0, 0, 0.1)
				if event.key == pygame.K_DOWN:
					cam.position += (0, 0, -0.1)
				# move ball
				if event.key == pygame.K_i:
					ball_position -= (0.1, 0, 0)
				if event.key == pygame.K_j:
					ball_position -= (0, 0.1, 0)
				if event.key == pygame.K_k:
					ball_position += (0.1, 0, 0)
				if event.key == pygame.K_l:
					ball_position += (0, 0.1, 0)
				# quit
				if event.key in (pygame.K_q, pygame.K_ESCAPE):
					quit_game = True
		
		# update screen
		pygame.display.flip()
	
	pygame.quit()
	