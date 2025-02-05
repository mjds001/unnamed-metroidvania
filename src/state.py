import pygame
from pytmx.util_pygame import load_pygame

from settings import *
from camera import Camera
from transition import Transition
from background import Background
from npc import NPC
from player import Player
from obstacles.wall import Wall
from obstacles.spike import Spike
from obstacles.one_way_platform import OneWayPlatform
from obstacles.moving_platform import MovingPlatform
from collider import Collider

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


class SplashScreen(State):

    def update(self, dt):
        if INPUTS['jump'] == True:
            Scene(self.game, '0', 'begin').enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLORS['blue'])
        self.game.render_text('PRESS SPACE TO START', COLORS['white'], (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

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
        # draw pause menu and make it semi transparent by adjusting the alpha
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


OBSTACLE_TYPES = {
    "wall": Wall,
    "spike": Spike,
    "moving_platform": MovingPlatform,
    "one_way_platform": OneWayPlatform
}

class Scene(State):

    def __init__(self, game, current_scene, entry_point):
        super().__init__(game)

        self.current_scene = current_scene
        self.entry_point = entry_point

        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        # add a custom attribute to the obstacle group so it can be identified later
        self.obstacle_sprites.is_obstacle_group = True
        self.exit_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame(f'assets/scenes/{self.current_scene}.tmx')
        self.width = self.tmx_data.width * TILESIZE
        self.height = self.tmx_data.height * TILESIZE
        self.camera = Camera(self)
        self.background = Background(self)
        self.transition = Transition(self)
        self.create_scene()

    def go_to_scene(self):
        Scene(self.game, self.new_scene, self.entry_point).enter_state()

    def create_scene(self):
        layers = {}
        for layer in self.tmx_data.layers:
            layers[layer.name] = layer

        if 'obstacles' in layers:
            layer = layers['obstacles']
            for x, y, surf in layer.tiles():
                gid = self.tmx_data.get_tile_gid(x, y, (layer.id - 1))
                tile = self.tmx_data.get_tile_properties_by_gid(gid)
                tile_type = tile.get('type')
                obstacle_class = OBSTACLE_TYPES[tile_type]
                obstacle_class([self.update_sprites, self.drawn_sprites, self.obstacle_sprites], pos=(x * TILESIZE, y * TILESIZE), surf= surf)

        if 'entries' in layers:
            for obj in self.tmx_data.get_layer_by_name('entries'):
                if obj.name == self.entry_point:
                    self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x,obj.y), 'ninja')
                    self.target = self.player

        if 'exits' in layers:
            for obj in self.tmx_data.get_layer_by_name('exits'):
                Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

        if 'entities' in layers:
             for obj in self.tmx_data.get_layer_by_name('entities'):
                 if obj.name == 'npc':
                    self.npc = NPC(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'npc')


    def update(self, dt):
        self.background.update(PHYSICS_DT, self.target)
        self.update_sprites.update(PHYSICS_DT)
        self.camera.update(PHYSICS_DT, self.target)
        self.transition.update(dt)
        if INPUTS['pause'] == True:
            Pause(self.game).enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        self.background.draw(screen)
        self.camera.draw(screen, self.drawn_sprites)
        self.transition.draw(screen)