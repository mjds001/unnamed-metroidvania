from settings import *
from states.scene import Scene
from states.state import State


class SplashScreen(State):

    def update(self, dt):
        if INPUTS['jump'] == True:
            Scene(self.game, '0', 'begin').enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLORS['blue'])
        self.game.render_text('PRESS SPACE TO START', COLORS['white'], (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))