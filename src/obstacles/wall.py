from obstacles.obstacle import Obstacle
from settings import *

import pygame


class Wall(Obstacle):

    def handle_collisions(self, axis, character):
        # handle horizontal collisions with a wall
        if axis == 'x':
            if (character.prev_hitbox.right - 1) <= self.hitbox.left <= character.hitbox.right: # character moving right
                character.hitbox.right = self.hitbox.left
            elif (character.prev_hitbox.left + 1) >= self.hitbox.right >= character.hitbox.left: # character moving left
                character.hitbox.left = self.hitbox.right
            elif character.hitbox.left <= self.hitbox.left <= character.hitbox.right:
                character.hitbox.right = self.hitbox.left
            elif character.hitbox.left <= self.hitbox.right <= character.hitbox.right:
                character.hitbox.left = self.hitbox.right
            character.on_wall = True
            # add frictional force for sliding on wall if the character is moving down
            if character.vel.y > 0 and character.name == 'ninja':
                character.y_forces.append(self.fric.y * character.vel.y)
            character.vel.x = 0
            character.rect.centerx = character.hitbox.centerx
        # handle vertical collisions with a wall
        elif axis == 'y':
            if (character.prev_hitbox.bottom - 1) <= self.hitbox.top <= character.hitbox.bottom: # falling
                character.hitbox.bottom = self.hitbox.top
                # wall applies normal force on character
                # make this force slightly less than gravity so there will still be some downward velocity
                character.y_forces.append(-GRAVITY*character.mass*0.99)
                # add frictional force for walking/running
                character.x_forces.append(self.fric.x * character.vel.x * character.mass)
                character.on_ground = True
            elif (character.prev_hitbox.top + 1) >= self.hitbox.bottom >= character.hitbox.top: # jumping
                character.hitbox.top = self.hitbox.bottom
            character.vel.y = 0
            character.rect.centery = character.hitbox.centery