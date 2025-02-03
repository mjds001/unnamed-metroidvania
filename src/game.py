import pygame
import sys
import os

from settings import *
from state import SplashScreen

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
        self.font = pygame.font.Font(FONT, TILESIZE)
        self.running = True
        self.fps = 60

        self.states = []
        self.splash_screen = SplashScreen(self)
        self.states.append(self.splash_screen)

    def render_text(self, text, color, pos, font_size = None, centered=True, font = None):
        if font == None:
            if font_size == None:
                font = self.font
            else:
                font = pygame.font.Font(FONT, font_size)
        surf = font.render(str(text), False, color)
        rect = surf.get_rect(center = pos) if centered else surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

    def get_images(self, path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            img = pygame.image.load(full_path).convert_alpha()
            images.append(img)
        return images

    def get_animations(self, path):
        animations = {}
        for file in os.listdir(path):
            animations[file] = []
        return animations

    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == Controls.JUMP.value:
                    INPUTS['jump'] = True
                if event.key == Controls.DASH.value:
                    INPUTS['dash'] = True
                if event.key == Controls.MOVE_LEFT.value:
                    INPUTS['left'] = True
                elif event.key == Controls.MOVE_RIGHT.value:
                    INPUTS['right'] = True
                elif event.key == Controls.DOWN.value:
                    INPUTS['down'] = True
                elif event.key == Controls.UP.value:
                    INPUTS['up'] = True
                if event.key == Controls.QUIT.value:
                    INPUTS['esc'] = True
                    self.running = False
                if event.key == Controls.PAUSE.value:
                    INPUTS['pause'] = True

            if event.type == pygame.KEYUP:
                if event.key == Controls.JUMP.value:
                    INPUTS['jump'] = False
                if event.key == Controls.DASH.value:
                    INPUTS['dash'] = False
                if event.key == Controls.MOVE_LEFT.value:
                    INPUTS['left'] = False
                elif event.key == Controls.MOVE_RIGHT.value:
                    INPUTS['right'] = False
                elif event.key == Controls.DOWN.value:
                    INPUTS['down'] = False
                elif event.key == Controls.UP.value:
                    INPUTS['up'] = False

    def reset_inputs(self):
        for key in INPUTS:
            INPUTS[key] = False

    def loop(self):
        while self.running:
            dt = self.clock.tick(self.fps)/1000
            self.get_inputs()
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.loop()