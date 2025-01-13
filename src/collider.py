import pygame
from settings import *


class Collider(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size, number):
        super().__init__(groups)
        self.image = pygame.Surface((size))
        self.rect = self.image.get_frect(topleft = pos)
        self.number = number