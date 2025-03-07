from obstacles.obstacle import Obstacle
from particles.fire_particle import FireParticle



class Fire(Obstacle):

    def __init__(self, scene, groups, pos, surf, z='obstacles', tile=None):
        pos = (pos[0], pos[1]-5)
        self.update_and_drawn_groups = [groups[0], groups[1]]
        super().__init__(scene, groups, pos, surf, z, tile)
        self.scene_frame_index = 0

    def update(self, dt):
        super().update(dt)
        self.animate()
        self.scene_frame_index += 1
        if self.scene_frame_index % 20 == 0:
            self.scene_frame_index = 0
            FireParticle(
                groups = self.update_and_drawn_groups,
                pos = self.rect.center
            )