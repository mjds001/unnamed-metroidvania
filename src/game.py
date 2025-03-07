import pygame
import sys
import os
import json

from settings import *
from states.splash_screen import SplashScreen
from states.scene import Scene


class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 512)
        self.init_sounds()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
        self.font = pygame.font.Font(FONT, TILESIZE)
        self.running = True
        self.fps = 60

        self.states = []
        self.splash_screen = SplashScreen(self)
        self.states.append(self.splash_screen)
        self.inventory = {}

    def init_sounds(self):
        # sound stuff
        self.sounds = {key: pygame.mixer.Sound(value) for key, value in SOUND_FILES.items()}
        for sound in self.sounds.values():
            sound.set_volume(0.1)
        self.sound_durations = {}
        for sound, wav in SOUND_FILES.items():
            audio = AudioSegment.from_file(wav)
            duration = len(audio) / 1000 # convert to seconds
            self.sound_durations[sound] = duration

    def render_text(self, text, color, pos, font_size = None, centered=True, font = None):
        if font == None:
            if font_size == None:
                font = self.font
            else:
                font = pygame.font.Font(FONT, font_size)
        surf = font.render(str(text), False, color)
        rect = surf.get_rect(center = pos) if centered else surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

    def save_game(self, scene):
        save_data = {
            "inventory": self.inventory,
            "current_scene": scene.current_scene,
            "entry_point": scene.entry_point
        }

        with open(SAVEPATH, "w") as file:
            json.dump(save_data, file, indent=4)

    def load_game(self, save_file=None):
        if save_file:
            with open(save_file, "r") as file:
                save_data = json.load(file)
            self.inventory = save_data['inventory']
            Scene(self, save_data['current_scene'], save_data['entry_point']).enter_state()
        else:
            Scene(self, 'house', 'begin').enter_state()
        self.reset_inputs()
    
    def get_images(self, path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if not full_path.lower().endswith('.png'):
                continue
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
                if event.key == Controls.THROW.value:
                    INPUTS['throw'] = True
                if event.key == Controls.QUIT.value:
                    INPUTS['esc'] = True
                    self.running = False
                if event.key == Controls.PAUSE.value:
                    INPUTS['pause'] = True
                if event.key == Controls.RESET.value:
                    INPUTS['reset'] = True

            if event.type == pygame.KEYUP:
                if event.key == Controls.JUMP.value:
                    INPUTS['jump'] = False
                if event.key == Controls.DASH.value:
                    INPUTS['dash'] = False
                if event.key == Controls.THROW.value:
                    INPUTS['throw'] = False
                if event.key == Controls.MOVE_LEFT.value:
                    INPUTS['left'] = False
                elif event.key == Controls.MOVE_RIGHT.value:
                    INPUTS['right'] = False
                elif event.key == Controls.DOWN.value:
                    INPUTS['down'] = False
                elif event.key == Controls.UP.value:
                    INPUTS['up'] = False
                if event.key == Controls.RESET.value:
                    INPUTS['reset'] = False

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