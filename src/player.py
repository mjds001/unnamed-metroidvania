from pygame.math import Vector2 as vec

from npc import NPC
from settings import *
from player_states import *


class Player(NPC):
    def __init__(self, game, scene, groups, pos, name, z='player'):
        super().__init__(game, scene, groups, pos, name, z)
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.7, -self.rect.height*0.2)
        self.ground_move_force = 3450
        self.air_move_force = self.ground_move_force*0.3
        self.max_speed = vec(210, 600)
        self.dash_mult = 1.5
        self.max_dash_speed = self.max_speed.x * self.dash_mult
        self.dash_force = self.ground_move_force * self.dash_mult
        self.jump_force = -25000
        # wall jump force is a vector bc we want the player to jump up and away from the wall
        self.wall_jump_force = vec(self.air_move_force*0.8, -self.air_move_force*0.8)
        self.state = Idle(self)

    def collisions(self, axis, group):
        for sprite in self.get_collide_list(group):
            if self.hitbox.colliderect(sprite.hitbox):
                sprite.handle_collisions(axis, self)
        
    def movement(self):
        if INPUTS['left']:
            if self.on_ground:
                self.x_forces.append(-self.ground_move_force)
            else:
                self.x_forces.append(-self.air_move_force)
        elif INPUTS['right']:
            if self.on_ground:
                self.x_forces.append(self.ground_move_force)
            else:
                self.x_forces.append(self.air_move_force)
        else:
            self.acc.x = 0

    def go_to_last_ground_pos(self):
        self.hitbox.center = self.last_on_ground_pos
        self.rect.center = self.hitbox.center
        self.vel = vec()
        self.acc = vec()

    def exit_scene(self):
        for exit in self.scene.exit_sprites:
            if self.hitbox.colliderect(exit.rect):
                self.scene.new_scene = exit.number
                self.scene.entry_point = self.scene.current_scene
                self.scene.transition.exiting = True

    def update(self, dt):
        self.exit_scene()
        if self.invincible_timer >= 0:
            self.invincible_timer -= dt
        super().update(dt)