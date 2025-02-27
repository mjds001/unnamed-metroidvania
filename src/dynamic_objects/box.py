from dynamic_objects.dynamic_object import DynamicObject
from characters.player_states import Crush, Push
from settings import *

import pygame


class Box(DynamicObject):
    """
    A class for a moveable box that the player can push
    """
    def __init__(self, game, scene, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='obstacles', custom_properties = None):
        super().__init__(game, scene, groups, pos, surf, z)
        self.fric = OBSTACLE_FRIC
        self.mass = 300
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0, -self.rect.height*0)


    def handle_collisions(self, axis, character):
        # character will be crushed if a box lands on top of them
        if character.z == 'player':
            if self.prev_hitbox.bottom -1 <= character.hitbox.top <= character.hitbox.bottom and character.state.__class__!= Crush: # box is falling
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
            elif (character.prev_hitbox.top + 1) >= self.hitbox.bottom >= character.hitbox.top: # jumping
                character.hitbox.top = self.hitbox.bottom
            character.vel.y = 0
            character.rect.centery = character.hitbox.centery
        if axis == 'x':
            if character.z == 'player' and character.state.__class__ != Push:
                character.change_state(Push(character))
            if (character.prev_hitbox.right - 1) <= self.hitbox.left <= character.hitbox.right:
                character.hitbox.right = self.hitbox.left
            elif (character.prev_hitbox.left + 1) >= self.hitbox.right >= character.hitbox.left: # character moving left
                character.hitbox.left = self.hitbox.right
            elif character.hitbox.left <= self.hitbox.left <= character.hitbox.right:
                #self.hitbox.left = character.hitbox.right
                character.hitbox.right = self.hitbox.left
            elif character.hitbox.left <= self.hitbox.right <= character.hitbox.right:
                #self.hitbox.right = character.hitbox.left
                character.hitbox.left = self.hitbox.right
            collide_force = character.acc.x * character.mass
            self.x_forces.append(collide_force)
            character.vel.x = 0
            character.rect.centerx = character.hitbox.centerx