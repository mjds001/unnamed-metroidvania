from obstacles.obstacle import Obstacle
from pygame.math import Vector2 as vec


class Spike(Obstacle):
    def __init__(self, groups, pos, surf, z='obstacles', tile = None):
        super().__init__(groups, pos, surf, z)
        self.hitbox = self.rect.copy().inflate(0,0)
        self.knockback_force = vec(10000, -5000)

    def handle_collisions(self, axis, character):
        #character.go_to_last_ground_pos()
        if character.invincible_timer <= 0:
            character.hit = True
            character.reset_position = True
            character.x_forces.append(-1*character.get_direction(return_int=True)*self.knockback_force.x)
            character.y_forces.append(self.knockback_force.y)