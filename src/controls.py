from enum import Enum
import pygame

class Controls(Enum):
    MOVE_LEFT = pygame.K_LEFT
    MOVE_RIGHT = pygame.K_RIGHT
    JUMP = pygame.K_SPACE
    DASH = pygame.K_z
    