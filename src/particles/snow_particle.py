from particles.particle import Particle
from settings import *

import random



class SnowParticle(Particle):
    def __init__(self, scene, groups, pos, vel, size, color=COLORS['white'], z='lit_particles'):
        self.scene = scene
        alpha = random.randint(20,255)
        color = (color[0], color[1], color[2], alpha)
        super().__init__(groups, pos, vel, size, color, z)
        self.shrink_rate = 0
        self.gravity = 0
        self.light_color = (20,20,50)
        self.light_size = self.size*2

    def update(self, dt):
        super().update(dt)
        if self.rect.centerx < 0 or self.rect.centerx > self.scene.width:
            self.kill()
        if self.rect.centery > self.scene.height:
            self.kill()
