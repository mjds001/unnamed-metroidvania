# class to handle dialogue cues which will be displayed at the bottom of the screen
# when the player is nearby an object that can be interacted with

import pygame
from settings import *

class DialogCue(pygame.sprite.Sprite):
    def __init__(self, game, text, groups, z='ui'):
        super().__init__(groups)
        self.text = text
        self.game = game
        self.font = pygame.font.Font(FONT, 12)
        self.visible = False
        self.box_rect = pygame.Rect(20, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 40, 80)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def render_text(self, text, screen):
        surf = self.font.render(str(text), False, color=COLORS['white'])
        rect = surf.get_rect(center=self.box_rect.center)
        screen.blit(surf, rect)

    def update(self, dt):
        pass

    def draw(self, screen):
        if self.visible:
            self.render_text(self.text, screen)