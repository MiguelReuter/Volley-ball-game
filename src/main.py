# encoding : UTF8

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # disable welcome message from pygame
import pygame

from Engine import GameEngine


if __name__ == "__main__":
	pygame.init()

	game_engine = GameEngine()
	game_engine.run()

	pygame.display.quit()
	pygame.quit()
	