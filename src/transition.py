import pygame

from settings import *

class Transition:
    def __init__(self, scene):
        self.fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.scene = scene
        self.exiting = False
        self.fade_in_speed = 200
        self.fade_out_speed = 1000
        self.alpha = 255

    def update(self, dt):
        if self.exiting:
            self.alpha = min(255, self.alpha + self.fade_out_speed*dt)
            if self.alpha >= 255:
                self.scene.go_to_scene()
        else:
            self.alpha = max(0, self.alpha - self.fade_in_speed * dt)

    def draw(self, screen):
        self.fade_surf.fill(COLORS['black'])
        self.fade_surf.set_alpha(self.alpha)
        screen.blit(self.fade_surf, (0,0))