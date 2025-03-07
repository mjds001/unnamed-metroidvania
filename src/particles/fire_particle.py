from particles.particle import Particle
from settings import *

import random
from pygame.math import Vector2 as vec



class FireParticle(Particle):
    def __init__(self, groups, pos, vel=None, size=None, color=COLORS['red'], z='lit_particles'):
        if vel is None:
            vel = vec(random.uniform(-75,75), random.uniform(-50,0))
        if size is None:
            size = random.randint(1,4)
        super().__init__(groups, pos, vel, size, color, z)
        self.light_color = (50,20,20)
        self.light_size = self.size*2
        self.gravity = 2
        self.shrink_rate = self.shrink_rate / 4

    def update(self, dt):
        super().update(dt)
        self.light_size = self.size*2
        self.vel.x += random.uniform(-5, 5)
        rand_num = random.randint(1,50)
        if rand_num == 1:
            self.vel.x *= -0.33
        if abs(self.vel.x) > 100:
            self.vel.x // 2