import pygame

from settings import *


class DynamicObject(pygame.sprite.Sprite):
    """
    A parent class for in game objects that are affected by physics and
    can interact with in game obstacles
    """
    def __init__(self, game, scene, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='obstacles'):
        super().__init__(groups)
        self.game = game
        self.scene = scene
        self.z = z
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(0,0)
        self.prev_hitbox = self.hitbox.copy()
        self.acc = vec()
        self.vel = vec()
        self.y_forces = []
        self.x_forces = []
        self.mass = 1
        self.on_ground = False

    def get_collide_list(self, group):
        collidable_list = pygame.sprite.spritecollide(self, group, False)
        return collidable_list
    
    def collisions(self, axis, group):
        for sprite in self.get_collide_list(group):
            if sprite is self:
                continue
            if self.hitbox.colliderect(sprite.hitbox):
                sprite.handle_collisions(axis, self)

    def physics(self, dt):
        # initialize this to false- collisions will change to true if found
        self.on_ground = False
        self.on_wall = False
        self.climbing = False
        # store the most recent hitbox to aid in colliison detection raycasting
        self.prev_hitbox = self.hitbox.copy()

        # x direction
        self.acc.x = (self.vel.x*AIR_FRIC.x + sum(self.x_forces)) / self.mass
        self.x_forces = []
        self.vel.x += self.acc.x * dt
        self.hitbox.centerx += self.vel.x * dt * PX_TO_M
        self.rect.centerx = self.hitbox.centerx 
        self.collisions('x', self.scene.obstacle_sprites)
        
        # y direction
        self.acc.y = GRAVITY + ((self.vel.y*AIR_FRIC.y + sum(self.y_forces)) / self.mass)
        self.y_forces = []
        self.vel.y += self.acc.y * dt
        self.hitbox.centery += self.vel.y * dt * PX_TO_M
        self.rect.centery = self.hitbox.centery 
        self.collisions('y', self.scene.obstacle_sprites)

    def update(self, dt):
        self.physics(dt)