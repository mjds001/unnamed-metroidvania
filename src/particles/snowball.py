from particles.particle import Particle
from settings import *

from pygame.math import Vector2 as vec
import random


class Snowball(Particle):
    """
    A particle subclass for the snowball the player can throw
    :direction: 1 for right, -1 for left
    """

    def __init__(self, groups, pos, direction, size = 7, color = COLORS['white'], z='particles'):
        vel = vec(300*direction, -75)
        self.all_groups = groups
        super().__init__(groups, pos, vel, size, color, z)
        self.shrink_rate = 0
        self.gravity = 7
        for group in groups:
            if getattr(group, 'is_drawn_sprites', False):
                self.drawn_sprites = group
                
    def update(self, dt):
        super().update(dt)
        for sprite in self.drawn_sprites:
            if sprite.z == 'player' or sprite.z == 'particles' or sprite.z == 'lit_particles' or sprite==self:
                continue
            if self.hitbox.colliderect(sprite.hitbox):
                # generate snow splash
                for n in range(1,8):
                    Particle(groups= self.all_groups,
                             pos= self.rect.center,
                             vel= vec(random.uniform(-150,150), random.uniform(-150,0)),
                             size= 3,
                             color= COLORS['white']
                             )
                self.kill()

