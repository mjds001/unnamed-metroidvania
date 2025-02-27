from obstacles.obstacle import Obstacle
from settings import *

import pygame

class OneWayPlatform(Obstacle):
    """
    These platforms allow the player to jump or move through them from below, but will
    act as a solid surface if the player is above.
    """
    def __init__(self, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='obstacles', tile = None):
        """
        metadata may vary depending on the obstacle type.
        At a minimum, metadata should include x, y, width, and height
        """
        super().__init__(groups, pos, surf, z)
        self.full_rect = self.image.get_rect(topleft = pos)
        self.bounding_rect = self.image.get_bounding_rect()
        self.hitbox = pygame.Rect(
            self.full_rect.x,
            self.full_rect.y,
            self.bounding_rect.width,
            self.bounding_rect.height
        )

    def handle_collisions(self, axis, character):
        # collision detection only happens if the player is above the platform
        if axis == 'y':
            if (character.prev_hitbox.bottom - 1) <= self.hitbox.top <= character.hitbox.bottom:
                character.hitbox.bottom = self.hitbox.top
                character.y_forces.append(-GRAVITY * 0.99 * character.mass)
                character.x_forces.append(self.fric.x * character.vel.x * character.mass)
                character.on_ground = True
                character.vel.y = 0
                character.rect.centery = character.hitbox.centery
        elif axis == 'x':
            # do nothing for horizontal collisions
            pass