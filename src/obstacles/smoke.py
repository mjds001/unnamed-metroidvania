from obstacles.obstacle import Obstacle


class Smoke(Obstacle):

    def __init__(self, scene, groups, pos, surf, z='obstacles', tile = None):
        # need to slightly adjust position because of the wal tiled handles
        # tile occupies multiple spaces
        super().__init__(scene, groups, pos, surf, z, tile)

    def update(self, dt):
        super().update(dt)
        self.animate()