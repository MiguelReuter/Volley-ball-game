# encoding : UTF-8

import pygame as pg
import pytest

from Settings import *
from Engine.Input import *


@pytest.yield_fixture()
def input_manager():
	# pygame has to be initialized to use event module
	pg.display.init()
	pg.display.set_mode([10, 10])  # dummy set mode
	
	input_manager = InputManager(None)
	yield InputManager(None)
	
	pg.quit()


def test_keyboard_press_key(input_manager):
	keyboard_device = KeyboardInputDevice(PlayerId.PLAYER_ID_ALL)
	input_manager.input_devices = [keyboard_device]

	# get first key
	key_code = list(keyboard_device.keys.keys())[0]
	
	assert keyboard_device.keys[key_code] == KeyState.RELEASED
	input_manager.update()
	assert keyboard_device.keys[key_code] == KeyState.RELEASED
	
	# press 'key_code' key
	event = pg.event.Event(pg.KEYDOWN)
	event.key = key_code
	pg.event.post(event)
	
	assert keyboard_device.keys[key_code] == KeyState.RELEASED  # input_manager is not updated yet
	input_manager.update()
	assert keyboard_device.keys[key_code] == KeyState.JUST_PRESSED
	input_manager.update()
	assert keyboard_device.keys[key_code] == KeyState.PRESSED
	input_manager.update()
	assert keyboard_device.keys[key_code] == KeyState.PRESSED
	
	# release 'key_code' key
	event = pg.event.Event(pg.KEYUP)
	event.key = key_code
	pg.event.post(event)
	
	assert keyboard_device.keys[key_code] == KeyState.PRESSED
	input_manager.update()
	assert keyboard_device.keys[key_code] == KeyState.JUST_RELEASED
	input_manager.update()
	assert keyboard_device.keys[key_code] == KeyState.RELEASED

	

	