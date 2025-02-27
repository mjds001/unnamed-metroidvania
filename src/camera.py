import pygame
from settings import *
from pygame.math import Vector2 as vec


class Camera(pygame.sprite.Group):
    
    def __init__(self, scene):
        self.offset = vec() 
        self.visible_window = pygame.FRect(0,0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.delay = 10 # add a slight delay so the camera follows just behind target
        self.scene_size = (scene.width, scene.height)
        self.player_highlight_radius = TILESIZE*6
        self.player_highlight = self.add_player_highlight()

    def add_player_highlight(self, color=(255,255,255), brightness=0.5):
        radius = self.player_highlight_radius
        surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        for y in range(radius*2):
            for x in range(radius*2):
                dist_to_center = ((x - radius)**2 + (y-radius)**2)**0.5
                if dist_to_center <= radius:
                    alpha = int(255*brightness * (1-(dist_to_center/radius)))
                    surf.set_at((x,y), (*color, alpha))
        return surf

    def update(self, dt, target):
        self.offset.x += (target.rect.centerx - SCREEN_WIDTH/2 - self.offset.x) * (self.delay * dt)
        self.offset.y += (target.rect.centery - SCREEN_HEIGHT/2 - self.offset.y) * (self.delay * dt)

        self.offset.x = max(0, min(self.offset.x, self.scene_size[0] - SCREEN_WIDTH))
        self.offset.y = max(0, min(self.offset.y, self.scene_size[1] - SCREEN_HEIGHT))
        self.visible_window.x = self.offset.x
        self.visible_window.y = self.offset.y

    def draw(self, screen, group):
        for layer in LAYERS:
            if layer == 'lit_particles':
                for sprite in group:
                    if self.visible_window.colliderect(sprite.rect) and sprite.z == layer:
                        offset = sprite.rect.topleft - self.offset
                        screen.blit(sprite.image, offset)
                        # add a backlight to the particles
                        pos = (sprite.rect.centerx - sprite.light_size//2, sprite.rect.centery - sprite.light_size//2) - self.offset
                        screen.blit(circle_surf(sprite.light_size, sprite.light_color), pos, special_flags = pygame.BLEND_RGB_ADD)
            elif layer == 'background':
                for sprite in group:
                    # draw the player highlight as part of the background
                    if sprite.z == 'player':
                        offset = sprite.rect.topleft - self.offset
                        screen.blit(self.player_highlight,
                                    offset - vec(self.player_highlight_radius - sprite.rect.width/2, self.player_highlight_radius - sprite.rect.height/2),
                                    )
                    if self.visible_window.colliderect(sprite.rect) and sprite.z == layer:
                        offset = sprite.rect.topleft - self.offset
                        screen.blit(sprite.image, offset)
            else:
                for sprite in group:
                    if self.visible_window.colliderect(sprite.rect) and sprite.z == layer:
                        offset = sprite.rect.topleft - self.offset
                        screen.blit(sprite.image, offset)
                        #pygame.draw.rect(screen, (255,0,0), sprite.hitbox, 1)


def circle_surf(diameter, color):
    surf = pygame.Surface((diameter, diameter))
    pygame.draw.circle(surf, color, (diameter // 2, diameter // 2), diameter // 2)
    surf.set_colorkey((0,0,0))
    return surf