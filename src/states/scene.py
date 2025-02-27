from settings import *
from appendix import *
from camera import Camera
from transition import Transition
from backgrounds.parallax_background import ParallaxBackground
from backgrounds.background import Background
from backgrounds.snow_background import SnowBackground
from characters.player import Player
from collider import Collider
from states.state import State
from states.pause import Pause

import pygame
from pytmx.util_pygame import load_pygame


class Scene(State):

    def __init__(self, game, current_scene, entry_point):
        super().__init__(game)

        self.current_scene = current_scene
        self.entry_point = entry_point

        # save the current game
        self.game.save_game(self)

        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.dialog = pygame.sprite.Group()
        self.spawn_queue = []
        # add a custom attribute to the obstacle group so it can be identified later
        self.obstacle_sprites.is_obstacle_group = True
        self.update_sprites.is_update_sprites = True
        self.drawn_sprites.is_drawn_sprites = True
        self.dialog.is_dialog = True
        self.exit_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame(f'assets/scenes/{self.current_scene}.tmx')
        self.width = self.tmx_data.width * TILESIZE
        self.height = self.tmx_data.height * TILESIZE
        self.camera = Camera(self)
        #self.background = ParallaxBackground(self)
        #self.background = Background(self)
        self.background = SnowBackground(self)
        self.transition = Transition(self)
        self.create_scene()

    def go_to_scene(self):
        Scene(self.game, self.new_scene, self.entry_point).enter_state()

    def reset_scene(self):
        Scene(self.game, self.current_scene, self.entry_point).enter_state()

    def create_scene(self):
        layers = {}
        for layer in self.tmx_data.layers:
            layers[layer.name] = layer

        if 'obstacles' in layers:
            layer = layers['obstacles']
            for x, y, surf in layer.tiles():
                gid = self.tmx_data.get_tile_gid(x, y, (layer.id - 1))
                tile = self.tmx_data.get_tile_properties_by_gid(gid)
                animation = tile['frames']
                if animation:
                    surf = []
                    for frame in animation:
                        image = self.tmx_data.get_tile_image_by_gid(frame.gid)
                        surf.append(image)
                tile_type = tile.get('type')
                if tile_type in OBSTACLES:
                    obstacle_class = OBSTACLES[tile_type]
                    obstacle_class([self.update_sprites, self.drawn_sprites, self.obstacle_sprites], pos=(x * TILESIZE, y * TILESIZE), surf= surf, tile = tile)
                elif tile_type in DYNAMIC_OBJECTS:
                    obj_class = DYNAMIC_OBJECTS[tile_type]
                    obj_class(self.game, self, [self.update_sprites, self.drawn_sprites, self.obstacle_sprites], pos=(x * TILESIZE, y * TILESIZE), surf= surf)
                elif tile_type in ITEMS:
                    # only render the item if it is not already in the player inventory
                    if tile_type not in self.game.inventory:
                        obj_class = ITEMS[tile_type]
                        obj_class(self.game, self, [self.update_sprites, self.drawn_sprites, self.obstacle_sprites], pos=(x* TILESIZE, y * TILESIZE), surf= surf, tile=tile)
                else:
                    # default to just using obstacle base class
                    OBSTACLES['obstacle']([self.update_sprites, self.drawn_sprites, self.obstacle_sprites], pos=(x * TILESIZE, y * TILESIZE), surf= surf, tile = tile)

        if 'entries' in layers:
            for obj in self.tmx_data.get_layer_by_name('entries'):
                if obj.name == self.entry_point:
                    self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x,obj.y), 'santa_merry')
                    self.player.entrypoint = (obj.x, obj.y)
                    self.target = self.player

        if 'exits' in layers:
            for obj in self.tmx_data.get_layer_by_name('exits'):
                Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

        if 'entities' in layers:
             for obj in self.tmx_data.get_layer_by_name('entities'):
                obj_class = ENTITIES.get(obj.type)
                if obj_class:
                    obj_class(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), name=obj.name, custom_properties=obj.properties)

    def manage_spawn_queue(self, dt):
        to_remove = []
        for sprite in self.spawn_queue:
            sprite['time_to_spawn'] -= dt
            if sprite['time_to_spawn'] <= 0:
                sprite['obj_class'](*sprite['args'])
                to_remove.append(sprite)
        for sprite in to_remove:
            self.spawn_queue.remove(sprite)

    def update(self, dt):
        self.background.update(PHYSICS_DT, self.target)
        self.update_sprites.update(PHYSICS_DT)
        self.camera.update(PHYSICS_DT, self.target)
        self.dialog.update(PHYSICS_DT)
        self.transition.update(dt)
        self.manage_spawn_queue(dt)
        if self.game.states[-1] == self:
            if INPUTS['pause'] == True:
                Pause(self.game).enter_state()
                self.game.reset_inputs()
            if INPUTS['reset'] == True:
                self.reset_scene()

    def draw(self, screen):
        self.background.draw(screen)
        self.camera.draw(screen, self.drawn_sprites)
        for dialog in self.dialog:
            dialog.draw(screen)
        self.transition.draw(screen)