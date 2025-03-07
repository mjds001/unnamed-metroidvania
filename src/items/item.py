import pygame
import os

from settings import *



class Item(pygame.sprite.Sprite):
    """
    a base class for items that the player can equip or unequip once they're in
    inventory.
    """
    def __init__(self, game, scene, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='foreground', tile = None, name = None, image_path = None, description = None):
        super().__init__(groups)
        self.game = game
        self.scene = scene
        if isinstance(surf, list):
            self.frames = surf
            self.image = self.frames[0]
            self.frame_index = 0
        else:
            self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(0,0)
        self.z = z
        self.name = name
        self.image_path = image_path
        self.description = description
        self.equipped = False
        
        # add these params to control the item floating in the level before it has been obtained
        self.vel = vec(0,10)
        self.max_travel = 5
        self.base_y = self.rect.y
        self.precise_pos = vec(self.rect.x, self.rect.y)

    def handle_collisions(self, axis, player):
        if player.z != 'player':
            return
        if self.equipped:
            return
        else:
            self.game.inventory[self.name] = {
                'image_path': self.image_path,
                'description': self.description,
                'equipped': False
            }
            self.kill()

    def update(self, dt):
        """
        default to adding a floating affect for items that have not yet been added to the inventory
        """
        if self.equipped == False:
            self.precise_pos += self.vel * dt
            self.rect.x = round(self.precise_pos.x)
            self.rect.y = round(self.precise_pos.y)
            self.hitbox = self.rect.copy()
            if self.rect.y > self.base_y + self.max_travel:
                self.vel *= -1
            elif self.rect.y < self.base_y - self.max_travel:
                self.vel *= -1

