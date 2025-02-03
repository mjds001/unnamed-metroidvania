import pygame
from pygame.math import Vector2 as vec

from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, scene, groups, pos, name=None, z='entities'):
        super().__init__(groups)
        self.game = game
        self.scene = scene
        self.z = z
        self.name = name
        self.frame_index = 0
        if not name:
            self.image = pygame.Surface((TILESIZE, TILESIZE*1.5))
        else:
            self.import_images(f'assets/characters/{self.name}/')
            self.image = self.animations['idle_right'][self.frame_index].convert_alpha()
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.3, -self.rect.height*0.2)
        self.prev_hitbox = self.hitbox.copy() # this will later be used to store the previous timestep position
        self.move_force = 2300
        self.max_speed = vec(140, 600)
        self.gravity = 800
        self.acc = vec()
        self.vel = vec()
        self.y_forces = []
        self.x_forces = []

        self.on_ground = False
        self.on_wall = False
        self.hit = False
        self.invincible = False
        self.invincible_timer = 0
        self.reset_position = False
        self.direction = 1
        self.state = Idle()
        self.move = {
            'left': True,
            'right': False
        }

    def import_images(self, path):
        self.animations = self.game.get_animations(path)

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = self.game.get_images(full_path)

    def animate(self, state, fps, loop=True):
        self.frame_index += fps
        if self.frame_index >= len(self.animations[state]):
            if loop:
                self.frame_index = 0
            else:
                self.frame_index = len(self.animations[state]) - 1 # keep playing the last animation frame
        self.image = self.animations[state][int(self.frame_index)]
        if self.invincible_timer > 0 and self.frame_index % 2 == 0:
            # when the player has invincibility frames, flash the sprite image every other frame
            # but do not permanently change the image
            self.image = pygame.Surface((TILESIZE, TILESIZE*1.5))
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))
            self.image.set_alpha(100)

    def get_direction(self, return_int=False):
        if self.hit == True:
            # if the player was just hit we don't want them to turn around due to knockback
            pass
        elif self.vel.x > 0.1:
            self.direction = 1
        elif self.vel.x < -0.1:
            self.direction = -1
        elif self.on_wall:
            self.direction = -1*self.direction

        if return_int:
            return self.direction
        else:
            return 'right' if self.direction == 1 else 'left'
        
    def movement(self):
        if self.move['left']:
            self.x_forces.append(-self.move_force)
        elif self.move['right']:
            self.x_forces.append(self.move_force)
    
    def get_collide_list(self, group):
        collidable_list = pygame.sprite.spritecollide(self, group, False)
        return collidable_list
    
    def collisions(self, axis, group):
        for sprite in self.get_collide_list(group):
            if self.hitbox.colliderect(sprite.hitbox):
                if axis == 'x':
                    if self.vel.x >= 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.vel.x <=0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.on_wall = True
                    self.vel.x = 0
                    self.rect.centerx = self.hitbox.centerx
                if axis == 'y':
                    if self.vel.y >=0: # falling
                        self.hitbox.bottom = sprite.hitbox.top
                        self.y_forces.append(-self.gravity*0.99) # make this slightly less than g so we don't have 0 force
                        self.on_ground = True
                    if self.vel.y<=0: # jumping
                        self.hitbox.top = sprite.hitbox.bottom
                    self.vel.y = 0
                    self.rect.centery = self.hitbox.centery

    def physics(self, dt):
        # initialize this to false- collisions will change to true if found
        self.on_ground = False
        self.on_wall = False
        # store the most recent hitbox to aid in colliison detection raycasting
        self.prev_hitbox = self.hitbox.copy()

        # x direction
        self.acc.x = self.vel.x*AIR_FRIC.x + sum(self.x_forces)
        self.x_forces = []
        self.vel.x += self.acc.x * dt
        self.vel.x = max(-self.max_speed.x, min(self.vel.x, self.max_speed.x))
        self.hitbox.centerx += self.vel.x * dt
        self.rect.centerx = self.hitbox.centerx
        self.collisions('x', self.scene.obstacle_sprites)
        
        # y direction
        self.acc.y = self.gravity + self.vel.y*AIR_FRIC.y + sum(self.y_forces)
        self.y_forces = []
        self.vel.y += self.acc.y * dt
        self.vel.y = max(-self.max_speed.y, min(self.vel.y, self.max_speed.y))
        self.hitbox.centery += self.vel.y * dt
        self.rect.centery = self.hitbox.centery
        self.collisions('y', self.scene.obstacle_sprites)
        if self.on_ground == True and not self.hit:
            self.last_on_ground_pos = self.hitbox.center

    def change_state(self):
        new_state = self.state.enter_state(self)
        if new_state: 
            self.state = new_state
        else:
            self.state

    def update(self, dt):
        self.get_direction()
        self.change_state()
        self.state.update(dt, self)
       
class Idle():
    def enter_state(self, character):
        if abs(character.vel.x) > 1:
            return Run()

    def update(self, dt, character):
        character.animate(f'idle_{character.get_direction()}', 15*dt)
        character.movement()
        character.physics(dt)

class Run:
    def enter_state(self, character):
        if abs(character.vel.x) <= 1:
            return Idle()
        
    def update(self, dt, character):
        character.animate(f'run_{character.get_direction()}', 15*dt)
        character.movement()
        character.physics(dt)