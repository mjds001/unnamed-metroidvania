from obstacles.obstacle import Obstacle
from settings import *

import pygame


class Wall(Obstacle):

    def handle_collisions(self, axis, character):
        # handle horizontal collisions with a wall
        if axis == 'x':
            if character.vel.x >= 0: # character moving right
                character.hitbox.right = self.hitbox.left
            elif character.vel.x <=0: # character moving left
                character.hitbox.left = self.hitbox.right
            character.on_wall = True
            character.vel.x = 0
            character.rect.centerx = character.hitbox.centerx
        # handle vertical collisions with a wall
        elif axis == 'y':
            if character.vel.y >=0: # falling
                character.hitbox.bottom = self.hitbox.top
                # wall applies normal force on character
                # make this force slightly less than gravity so there will still be some downward velocity
                character.y_forces.append(-character.gravity*0.99)
                character.on_ground = True
            elif character.vel.y <= 0: # jumping
                character.hitbox.top = self.hitbox.bottom
            character.vel.y = 0
            character.rect.centery = character.hitbox.centery

    
    def handle_horizontal_collision(self, player):
        """
        Handle horizontal collisions with the player.
        """
        if player.vel_x > 0: # moving right
            player.rect.right = self.rect.left
            player.on_wall = True
            player.wall_direction = "right"
        elif player.vel_x < 0: # moving left
            player.rect.left = self.rect.right
            player.on_wall = True
            player.wall_direction = "left"
        player.vel_x = 0

    def handle_vertical_collision(self, player):
        """
        Handle vertical collisions with the player.
        """
        if player.vel_y > 0: # falling
            player.rect.bottom = self.rect.top
            player.on_ground = True
        elif player.vel_y < 0: # jumping
            player.rect.top = self.rect.bottom
        player.vel_y = 0