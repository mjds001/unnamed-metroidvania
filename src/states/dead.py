from settings import *
from states.state import State

class Dead(State):
    def update(self, dt):
        self.game.states[-2].update(dt)
        if INPUTS['reset'] == True:
            self.game.states[-2].reset_scene()
            self.game.reset_inputs()

    def draw(self, screen):
        self.game.states[-2].draw(screen)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay, (0,0))
        self.game.render_text('Looks like you died. Press R to reset.', COLORS['white'], (SCREEN_WIDTH/2, 75), font_size = 20)
