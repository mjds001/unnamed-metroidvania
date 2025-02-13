from dynamic_objects.dynamic_object import DynamicObject
from characters.player_states import Crush
from settings import *

import pygame


class Box(DynamicObject):
    """
    A class for a moveable box that the player can push
    """
    def __init__(self, game, scene, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='obstacles'):
        super().__init__(game, scene, groups, pos, surf, z)
        self.fric = OBSTACLE_FRIC
        self.mass = 300


    def handle_collisions(self, axis, character):
        # character will be crushed if a box lands on top of them
        if character.z == 'player':
            if self.vel.y > 0.1 and character.state.__class__!= Crush: # box is falling
                character.change_state(Crush(character))
                return
            if character.state.__class__ == Crush:
                return
        # vertical collisions with a box- it should behave like a wall
        if axis == 'y':
            if (character.prev_hitbox.bottom - 1) <= self.hitbox.top <= character.hitbox.bottom: # falling
                character.hitbox.bottom = self.hitbox.top
                # wall applies normal force on character
                # make this force slightly less than gravity so there will still be some downward velocity
                character.y_forces.append(-GRAVITY*0.99*character.mass)
                self.y_forces.append(GRAVITY * character.mass)
                # add frictional force for walking/running
                character.x_forces.append(self.fric.x * character.vel.x * character.mass)
                character.on_ground = True
            elif character.vel.y < 0: # jumping
                character.hitbox.top = self.hitbox.bottom
            character.vel.y = 0
            character.rect.centery = character.hitbox.centery
        if axis == 'x':
            if character.vel.x > 0: # character moving right
                character.hitbox.right = self.hitbox.left
            elif character.vel.x < 0: # character moving left
                character.hitbox.left = self.hitbox.right
            collide_force = character.acc.x * character.mass
            self.x_forces.append(collide_force)
            character.vel.x = 0
            character.rect.centerx = character.hitbox.centerx
        