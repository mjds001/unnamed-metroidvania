from enum import Enum
import pygame

class Controls(Enum):
    MOVE_LEFT = pygame.K_LEFT
    MOVE_RIGHT = pygame.K_RIGHT
    JUMP = pygame.K_SPACE
    DASH = pygame.K_z
    QUIT = pygame.K_ESCAPE

INPUTS = {
    'escape': False,
    'jump': False,
    'dash': False,
    'left': False,
    'right': False,
    'esc': False
}
    
TILESIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FONT = 'assets/fonts/dogica.ttf'
PHYSICS_DT = 1/60

COLORS = {
    'red': (255,100,100),
    'green': (100,255,100),
    'blue': (100,100,255),
    'black': (0,0,0),
    'white': (255, 255, 255)
}

LAYERS = [
    'background',
    'obstacles',
    'entities',
    'player',
    'particles',
    'foreground'
]

