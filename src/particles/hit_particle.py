import random
import pygame
from pygame.math import Vector2 as vec

from particles.particle import Particle


class HitParticle(Particle):
    def __init__(self, groups, pos, direction = None, color = (255,255,255), z='particles'):
        size = random.randint(4,6)
        if direction == None:
            vel_x = random.uniform(-200, 200)
        elif direction == 1:
            vel_x = random.uniform(0,200)
        elif direction == -1:
            vel_x = random.uniform(-200,0)
        vel = vec(
            vel_x,
            random.uniform(-200,0)
        )
        super().__init__(groups, pos, vel, size, color, z)

    def update(self, dt):
        self.vel.y += self.gravity
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        self.size = max(0, self.size - self.shrink_rate)
        if self.size <= 0:
            self.kill()
        else:
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, self.color, ((self.size / 2), (self.size / 2)), int(self.size // 2))
            self.rect = self.image.get_rect(center=self.rect.center)