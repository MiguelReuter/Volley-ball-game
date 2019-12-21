# encoding : UTF-8

import numpy
import pygame as pg
from pygame.locals import *


def find_coeffs(pa, pb):
	matrix = []
	for p1, p2 in zip(pa, pb):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

	A = numpy.matrix(matrix, dtype=numpy.float)
	B = numpy.array(pb).reshape(8)

	res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
	return numpy.array(res).reshape(8)


def apply_perspective(pos, coeffs):
	x, y = pos
	x_out = (coeffs[0] * x + coeffs[1] * y + coeffs[2]) / (coeffs[-2] * x + coeffs[-1] * y + 1)
	y_out = (coeffs[3] * x + coeffs[4] * y + coeffs[5]) / (coeffs[-2] * x + coeffs[-1] * y + 1)

	return x_out, y_out


def apply_perspective_on_surface(surf_a, coeffs):
	r_a = surf_a.get_rect()
	corners_a = [r_a.topleft, r_a.topright, r_a.bottomright, r_a.bottomleft]

	corners_b = [apply_perspective(p_a, coeffs) for p_a in corners_a]
	size_b = [max(p_b[0] for p_b in corners_b) - min(p_b[0] for p_b in corners_b),
			  max(p_b[1] for p_b in corners_b) - min(p_b[1] for p_b in corners_b)]
	rx, ry = min(p_b[0] for p_b in corners_b), min(p_b[1] for p_b in corners_b)
	surf_b = pg.Surface(size_b)
	arr_b = pg.PixelArray(surf_b)

	for i in range(surf_a.get_size()[0]):
		for j in range(surf_a.get_size()[1]):
			col_ij = surf_a.get_at((i, j))
			x_b, y_b = apply_perspective((i, j), coeffs)
			x_b, y_b = int(x_b - rx), int(y_b - ry)
			arr_b[x_b, y_b] = col_ij

	arr_b.close()
	return surf_b


def create_grid_surface(w, h, d):
	surf = pg.Surface((w, h))
	surf.fill((255, 0, 0))

	for i in range(w // d + 1):
		for j in range(h // d + 1):
			if (i + j) % 2 == 0:
				r = pg.Rect(i * d, j * d, d, d)
				surf.fill((0, 0, 255), r)
	return surf


if __name__ == "__main__":
	w = 500
	h = 500
	d = 10

	pa = [(0, 0), (w, 0), (w, h), (0, h)]
	pb = [(w/4, h/4), (3*w/4, h/4), (w, h), (0, h)]

	coeffs = find_coeffs(pa, pb)
	print("coeffs: ", coeffs)

	# surfaces
	pg.init()
	screen = pg.display.set_mode((w, h))

	img = create_grid_surface(w, h, 10)

	# img_b perspective
	img_b = apply_perspective_on_surface(img, coeffs)

	screen.blit(img_b, pg.Rect((0, 0), img_b.get_size()))
	#screen.blit(img, pg.Rect(0, 0, w, h))

	pg.display.flip()

	# loop, escape or close window to quit
	done = False
	while not done:
		for ev in pg.event.get():
			if ev.type == KEYDOWN:
				if ev.key == K_ESCAPE:
					done = True
			elif ev.type == QUIT:
				done = True
	pg.quit()
