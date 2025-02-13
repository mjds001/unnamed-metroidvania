import pygame
from pytmx.util_pygame import load_pygame

from settings import *



class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def enter_state(self):
        if len(self.game.states) > 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def exit_state(self):
        self.game.states.pop()

    def update(self, dt):
        pass

    def draw(self, screen):
        pass


class Pause(State):

    def __init__(self, game):
        super().__init__(game)
        self.options = PLAYER_ATTRIBUTES.keys()
        self.selected_index = 0

    def update(self, dt):
        if INPUTS['pause'] == True:
            self.game.states.pop()
            self.game.reset_inputs()
        
        if INPUTS['down']:
            self.selected_index = min(max(self.selected_index + 1, 0), len(self.options) - 1)
            self.game.reset_inputs()
        if INPUTS['up']:
            self.selected_index = min(max(self.selected_index - 1, 0), len(self.options) - 1)
            self.game.reset_inputs()

    def draw(self, screen):
        # continue showing the previous state
        self.game.states[-2].draw(screen)
        # draw pause menu
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        self.game.render_text('PAUSED', COLORS['white'], (SCREEN_WIDTH/2, 75), font_size = 20)
        # display the player attributes from settings file
        for i, attr in enumerate(PLAYER_ATTRIBUTES.keys()):
            self.game.render_text(f'{attr}: {PLAYER_ATTRIBUTES[attr]}', COLORS['white'], (SCREEN_WIDTH/2, 100 + i * 25), font_size = 20)
            # highlight the selected option
            if i == self.selected_index:
                self.game.render_text(f'{attr}: {PLAYER_ATTRIBUTES[attr]}', COLORS['yellow'], (SCREEN_WIDTH/2, 100 + i * 25), font_size = 20)




