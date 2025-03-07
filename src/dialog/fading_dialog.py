import pygame

from settings import *



class FadingDialog(pygame.sprite.Sprite):
    """
    This is dialog that will display on the screen and then fade after a specificed amount of time.
    To be used, for example, when a player enters a new region of the map.
    """
    def __init__(self, game, text, groups, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), size = 32, color = COLORS['black'], fade_time = 2):
        super().__init__(groups)
        self.text = text
        self.pos = pos
        self.color = color
        self.game = game
        self.size = size
        self.font = pygame.font.Font(FONT, self.size)
        self.fade_time = fade_time
        self.fading = False
        self.alpha = 255

    def render_text(self, text, screen):
        surf = self.font.render(str(text), False, color=self.color)
        surf.set_alpha(self.alpha)
        rect = surf.get_rect(center=self.pos)
        screen.blit(surf, rect)

    def update(self, dt):
        if self.fade_time > 0:
            self.fade_time -= dt
        else:
            self.alpha -= 5
            if self.alpha <=0:
                self.kill()

    def draw(self, screen):
        self.render_text(self.text, screen)