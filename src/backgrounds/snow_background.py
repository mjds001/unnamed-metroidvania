from particles.snow_particle import SnowParticle
from backgrounds.background import Background
from pygame.math import Vector2 as vec


import random


class SnowBackground(Background):

    def __init__(self, scene):
        super().__init__(scene)
        # generate snow particles
        for x in range(1,100):
            SnowParticle(scene = self.scene,
                         groups = [scene.update_sprites, scene.drawn_sprites],
                         pos = (random.randint(0, self.scene.width), random.randint(0, self.scene.height)),
                         vel = vec(random.uniform(-10,10),random.uniform(35,110)),
                         size = random.randint(2,5)
            )
        self.frame_index = 0


    def update(self, dt, target):
        self.frame_index += 1
        if self.frame_index % 4 == 0:
            self.frame_index = 0
            SnowParticle(
                scene = self.scene,
                groups = [self.scene.update_sprites, self.scene.drawn_sprites],
                pos = (random.randint(0,self.scene.width), 0),
                vel = vec(random.uniform(-10,10),random.uniform(35,110)),
                size = random.randint(2,5)
            )