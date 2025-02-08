import pygame
import os

from settings import *

class ParallaxBackground():
    def __init__(self, scene, brighten=False):
        self.base_path = 'assets/backgrounds/cave'
        self.scene = scene
        self.brighten = brighten
        self.bg_images = self.get_bg_images(self.base_path)
        self.bg_images = self.scale_bg_images()
        if self.brighten:
            self.white_overlay = pygame.Surface((scene.width, scene.height), pygame.SRCALPHA)
            self.white_overlay.fill(COLORS['white'])
            self.white_overlay.set_alpha(5)
        self.image_width = self.bg_images[0].get_width()
        self.image_repetitions = 4
        self.scroll = self.image_width * (self.image_repetitions-2)/2

    
    def get_bg_images(self, path):
        try:
            images = [f for f in os.listdir(path)]
        except FileNotFoundError:
            print(f'error: The folder {path} could not be found')

        loaded_images = []
        for image in images:
            loaded_image = pygame.image.load(f'{path}/{image}').convert_alpha()
            loaded_images.append(loaded_image)

        return loaded_images
    
    def scale_bg_images(self):
        images = self.bg_images
        scaled_images = []
        og_width, og_height = images[0].get_size()
        scale_factor = self.scene.height / og_height
        for image in images:
            new_width = int(og_width * scale_factor)
            scaled_image = pygame.transform.smoothscale(image, (new_width, self.scene.height))
            scaled_images.append(scaled_image)
        return scaled_images
    
    def update(self, dt, target):
        self.scroll += target.vel.x * dt / 3
    
    def draw(self, screen):
        for x in range(self.image_repetitions):
            layer_speed = 1
            for image in self.bg_images:
                screen.blit(image, ((x * self.image_width) - self.scroll * layer_speed, 0))
                if self.brighten:
                    screen.blit(self.white_overlay, (0,0))
                layer_speed += 0.2