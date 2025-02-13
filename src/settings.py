from enum import Enum
import pygame
from pygame.math import Vector2 as vec


class Controls(Enum):
    MOVE_LEFT = pygame.K_LEFT
    MOVE_RIGHT = pygame.K_RIGHT
    DOWN = pygame.K_DOWN
    UP = pygame.K_UP
    JUMP = pygame.K_SPACE
    THROW = pygame.K_f
    DASH = pygame.K_z
    QUIT = pygame.K_ESCAPE
    PAUSE = pygame.K_p
    RESET = pygame.K_r

INPUTS = {
    'escape': False,
    'jump': False,
    'dash': False,
    'left': False,
    'right': False,
    'down': False,
    'up': False,
    'esc': False,
    'pause': False,
    'throw': False,
    'reset': False
}
    
TILESIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FONT = 'assets/fonts/dogica.ttf'

# physics
PHYSICS_DT = 1/60
GRAVITY = 10 # m/s^2
AIR_FRIC = vec(-1,-1)
PX_TO_M = 80 # in game conversion from pixels to meters to try to make the physics make some intuitive sense
OBSTACLE_FRIC = vec(-15,-5)

COLORS = {
    'red': (255,100,100),
    'green': (100,255,100),
    'blue': (100,100,255),
    'black': (0,0,0),
    'white': (255, 255, 255),
    'yellow': (255, 255, 100)
}

LAYERS = [
    'background',
    'obstacles',
    'entities',
    'player',
    'particles',
    'foreground',
    'ui'
]

# player attributes
PLAYER_ATTRIBUTES = {
    'max_speed': vec(210,600),
    'ground_move_force': 3450,
    'jump_force': -25000
}