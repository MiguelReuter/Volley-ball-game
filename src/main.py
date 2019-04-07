# encoding : UTF8

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # disable welcome message from pygame
import pygame

from Engine import *


if __name__ == "__main__":
	pygame.init()
	#pygame.key.set_repeat(10)

	game_engine = GameEngine()
	game_engine.run()

	pygame.display.quit()
	pygame.quit()
	