from settings import *
from obstacles.one_way_platform import OneWayPlatform

import pygame
import random


class MovingPlatform(OneWayPlatform):
    def __init__(self, groups, pos, surf, z='obstacles', tile = None):
        super().__init__(groups, pos, surf, z)
        self.vel = 60
        self.last_pos = self.rect.copy() # store the previous position
        for group in groups:
            if getattr(group, 'is_obstacle_group', False):
                self.obstacle_sprites = group
        self.collidables = []
    
    def handle_collisions(self, axis, character):
        super().handle_collisions(axis, character)
        if character.on_ground and axis == 'y':
            character.hitbox.centerx += self.rect.centerx - self.last_pos.centerx
            character.rect.centerx = character.hitbox.centerx

    def update(self, dt):
        # on the first frame, identify any obstacles in the platforms line of movement that it might collide with later
        # this will save compute time so we don't have to check colllisions with every obstacle every frame
        # this can't be done during init method b/c the full sprite group hasn't populated yet
        if len(self.collidables) == 0:
            for sprite in self.obstacle_sprites:
                if sprite is self:
                    continue
                if (sprite.hitbox.top <= self.hitbox.top < sprite.hitbox.bottom) or (sprite.hitbox.top < self.hitbox.bottom <= sprite.hitbox.bottom):
                    self.collidables.append(sprite)
        for sprite in self.collidables:
            if sprite.hitbox.colliderect(self.hitbox):
                self.vel = -1*self.vel

        self.last_pos = self.rect.copy()
        self.hitbox.centerx += round(self.vel * dt)
        self.rect.centerx = self.hitbox.centerx
