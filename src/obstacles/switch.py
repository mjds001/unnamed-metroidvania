from obstacles.obstacle import Obstacle
from settings import *

import pygame


class Switch(Obstacle):

    def __init__(self, groups, pos, surf, z='obstacles', tile = None):
        # the surf passed in will contain image for button pressed and unpressed
        super().__init__(groups, pos, surf, z)
        self.bounding_rect = self.frames[1].get_bounding_rect()
        self.hitbox = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.bounding_rect.width,
            self.bounding_rect.height
        )
        self.hitbox.bottom = self.rect.bottom
        # tile should have custom property specifying the initial switch position
        # switch positions are 'left' (frame 0), 'center' (frame 1 or 3), 'right' (frame 2)
        init_positions = {
            'left': 0,
            'center': 1,
            'right': 2
        }
        self.positions = {
            0: 'left',
            1: 'center',
            2: 'right',
            3: 'center'
        }
        if 'init_pos' in tile:
            self.frame_index = init_positions[tile['init_pos']]
        else:
            self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def handle_collisions(self, axis, character):
        if character.z != 'player':
            return
        if INPUTS['up']:
            INPUTS['up'] = False
            self.frame_index += 1
            if self.frame_index > len(self.frames) - 1:
                self.frame_index = 0
            self.image = self.frames[self.frame_index]

    def get_position(self, return_int=False):
        if return_int:
            return self.frame_index
        else:
            return self.positions[self.frame_index]