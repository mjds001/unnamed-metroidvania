from settings import *


class Background():
    def __init__(self, scene, color=COLORS['blue']):
        self.scene = scene
        self.color = color

    def update(self, dt, target):
        pass

    def draw(self, screen):
        screen.fill(self.color)