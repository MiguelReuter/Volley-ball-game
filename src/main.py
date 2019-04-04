# encoding : UTF8

from Engine.game_engine import *

import pygame

if __name__ == "__main__":
	pygame.init()
	pygame.key.set_repeat(10)
	
	game_engine = GameEngine()
	game_engine.run()
	
	print("exiting game...")
	pygame.display.quit()
	pygame.quit()
	print("exit game")
	