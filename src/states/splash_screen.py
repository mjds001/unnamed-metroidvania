from settings import *
from states.state import State

import os


class SplashScreen(State):

    def __init__(self, game):
        super().__init__(game)
        self.selected_index = 0
        if os.path.exists(SAVEPATH):
            self.text = ['NEW GAME', 'CONTINUE']
        else:
            self.text = ['NEW GAME']
        self.total_options = len(self.text)
        self.option_font_size = 32
        self.select_color = COLORS['black']

    def update(self, dt):
        if INPUTS['jump'] == True:
            if self.text[self.selected_index] == 'NEW GAME':
                self.game.load_game()
            elif self.text[self.selected_index] == 'CONTINUE':
                self.game.load_game(save_file=SAVEPATH)
        if INPUTS['up']:
            self.selected_index = (self.selected_index - 1) % self.total_options
            self.game.reset_inputs()
        if INPUTS['down']:
            self.selected_index = (self.selected_index + 1) % self.total_options
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLORS['blue'])
        for i in range(self.total_options):
            if i == self.selected_index:
                pygame.draw.rect(screen, self.select_color, (0, 200 + self.option_font_size*2*i - self.option_font_size, SCREEN_WIDTH, self.option_font_size*2))
            self.game.render_text(self.text[i], COLORS['white'], (SCREEN_WIDTH / 2, 200 + self.option_font_size*2*i), font_size = self.option_font_size)
        self.game.render_text('This is a game.', COLORS['white'], (SCREEN_WIDTH / 2, 100))
        self.game.render_text('Press space to select', COLORS['white'], (SCREEN_WIDTH / 2, SCREEN_HEIGHT-50), font_size=15)


