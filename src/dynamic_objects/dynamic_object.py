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
        self.name = None
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
        self.tipping = False
        self.angle = 0
        self.tip_direction = 0
        self.support_threshold = 0.4
        self.original_image = self.image.copy()

    def get_collide_list(self, group):
        collidable_list = pygame.sprite.spritecollide(self, group, False)
        return collidable_list
    
    def collisions(self, axis, group):
        for sprite in self.get_collide_list(group):
            if sprite is self:
                continue
            bottom_rect = pygame.Rect(self.hitbox.left, self.hitbox.bottom - 1, self.hitbox.width, 2)
            if bottom_rect.colliderect(sprite.hitbox) and axis == 'y':
                self.check_support(sprite)
            if self.hitbox.colliderect(sprite.hitbox):
                sprite.handle_collisions(axis, self)

    def check_support(self, sprite):
        overlap = min(self.hitbox.right, sprite.hitbox.right) - max(self.hitbox.left, sprite.hitbox.left)
        self.support_area += max(0, overlap)

        # Check if left and right edges are supported
        if self.hitbox.left < sprite.hitbox.right and self.hitbox.left > sprite.hitbox.left:
            self.left_support = True
            self.right_edge = sprite.hitbox.right
        if self.hitbox.right > sprite.hitbox.left and self.hitbox.right < sprite.hitbox.right:
            self.right_support = True
            self.left_edge = sprite.hitbox.left

    def handle_tipping(self):
        support_ratio = self.support_area / self.hitbox.width
        if support_ratio < self.support_threshold and not (self.right_support and self.left_support):
            self.tipping = True
            self.angle += 2 * self.tip_direction
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_frect(center = self.hitbox.center)
            if not self.on_ground:
                return
            # Determine tipping direction: if the right side is unsupported, tip right (+1), otherwise left (-1)
            if not self.right_support:
                self.tip_direction = -1  # Tip to the right
                if abs(self.angle) > 15: # initiate tip
                    self.hitbox.left = self.right_edge
                    self.hitbox.bottom += 2
            elif not self.left_support:
                self.tip_direction = 1  # Tip to the left
                if abs(self.angle) > 15: # initiate tip
                    self.hitbox.right = self.left_edge
                    self.hitbox.bottom += 2
        else:
            self.tipping = False
            self.image = self.original_image
            self.rect = self.image.get_frect(center = self.hitbox.center)
            self.tip_direction = 0
            self.angle = 0  # Reset angle if stable

    def physics(self, dt):
        # initialize this to false- collisions will change to true if found
        self.on_ground = False
        self.on_wall = False
        self.climbing = False
        self.left_support = False
        self.right_support = False
        self.support_area = 0

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
        self.handle_tipping()