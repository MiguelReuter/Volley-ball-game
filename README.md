**WIP** : Simple 2D retro Volley-ball game written from scratch with Pygame and Python3.

Check [Projects](https://github.com/MiguelReuter/Volley-ball-game/projects) page on Github to see progress !


# Overview

## Features

- Debug display with simple shapes, not sprites yet
- Play against a **human player** or a **bot** !
- Basic actions:
    - move
    - jump
    - smash
    - serve
    - throw ball
    - dive
    - quit and pause game
    - move camera (debug purpose)

Notes:

1. The target ball position is **controllable** in these actions :
     - **throw**
     - **smash** (depth only)
     - **serve**
2. You must hardcode in `src/Engine/game_engine.py` in `create` method if character 2 is controllable by a joystick or by Artifial Intelligence :
     - to play against AI: `char2 = Character((0, 5, 0), player_id=AIId.AI_ID_1, is_in_left_side=False)`
     - to play against a human player (joystick needed): `char2 = Character((0, 5, 0), player_id=PlayerId.PLAYER_ID_2, is_in_left_side=False)`
3. Game rules are not implemented yet

## Demo
### Throw ball
<img src="doc/throw.gif" height="400" />

### Smash
<img src="doc/smash.gif" height="400" />

### Dive
<img src="doc/dive.gif" height="400" />

### Serve
<img src="doc/serve.gif" height="400" />

### Collisions with net
<img src="doc/net_collision_1.gif" height="400" /> <img src="doc/net_collision_2.gif" height="400" />


## Controls

Keyboard and Gamepad are supported. For gamepad, button binds could be different depending on your device button layout.

| Key *(keyboard)*| Button *(Gamepad)*| Action                                    |
|---------------- |------------------ |------------------------------------------ |
| ZQSD            | POV, D-PAD        | **Move** or **Aim** during ball throwing  |
| I               | 2                 | **Jump**                                  |
| J               | 1                 | **Throw** ball or **Smash**               |
| L               | 3                 | **Dive** to catch up ball (after smash...)|
| Arrow Keys      | Right joystick    | **Move** camera                           |
| Space bar       | 4                 | **Re-throw** ball                         |
| Esc.            | 9                 | **Quit** game                             |
| P               | 10                | **Pause** game (not implemented yet)      |


---

# Dependencies
- python3
- pygame 1.9.5
- pytest to run tests (optional)

# Launch game
```
python3 src/main.py
```

# Run tests (optional)
```
py.test .
```

# Licence

The code is under the MIT license terms.

<!-- Required extensions: pymdownx.betterem, pymdownx.tilde, pymdownx.emoji, pymdownx.tasklist, pymdownx.superfences -->