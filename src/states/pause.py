from states.state import State
from settings import *
from appendix import *

import pygame


class Pause(State):

    def __init__(self, game):
        super().__init__(game)
        self.options = PLAYER_ATTRIBUTES.keys()
        self.selected_index = 0
        self.rows = 3
        self.cols = 4
        self.total_slots = self.rows * self.cols
        self.box_size = (80,80)
        self.margin = 20
        self.menu_pos = (50,100) # top left corner of the menu
        self.menu_width = (self.box_size[0] + self.margin) * self.cols + self.margin
        self.menu_height = (self.box_size[1] + self.margin) * self.rows + self.margin

        self.surfs = {}
        self.inventory_items = list(self.game.inventory.keys())
        for item, info in self.game.inventory.items():
            surf = pygame.image.load(info['image_path'])
            self.surfs[item] = surf

    def update(self, dt):
        if INPUTS['pause'] == True:
            self.game.states.pop()
            self.game.reset_inputs()
        
        if INPUTS['down']:
            self.selected_index = (self.selected_index + self.cols) % self.total_slots
            self.game.reset_inputs()
        if INPUTS['up']:
            self.selected_index = (self.selected_index - self.cols) % self.total_slots
            self.game.reset_inputs()
        if INPUTS['left']:
            self.selected_index = (self.selected_index - 1) % self.total_slots
            self.game.reset_inputs()
        if INPUTS['right']:
            self.selected_index = (self.selected_index + 1) % self.total_slots
            self.game.reset_inputs()
        if INPUTS['throw']:
            self.game.reset_inputs()
            if self.selected_index >= len(list(self.game.inventory.keys())):
                pass
            else:
                item = self.inventory_items[self.selected_index]
                if self.game.inventory[item]['equipped'] == True:
                    self.unequip_item(item)
                elif self.game.inventory[item]['equipped'] == False:
                    self.equip_item(item)

    def draw(self, screen):
        # continue showing the previous state
        self.game.states[-2].draw(screen)
        # draw pause menu
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        self.game.render_text('PAUSED', COLORS['white'], (SCREEN_WIDTH/2, 75), font_size = 20)
        
        
        for i in range(self.total_slots):
            # Calculate position for each item box
            box_x = self.menu_pos[0] + self.margin + (i % self.cols) * (self.box_size[0] + self.margin)
            box_y = self.menu_pos[1] + self.margin + (i // self.cols) * (self.box_size[1] + self.margin)

            # Highlight selected item
            box_color = (255, 255, 255) if i == self.selected_index else (150, 150, 150)
            pygame.draw.rect(screen, box_color, (box_x, box_y, *self.box_size))
            pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, *self.box_size), 2)  # Border

            # Draw item image if an item exists in this slot
            if i < len(self.inventory_items):
                item_name = self.inventory_items[i]
                item_image = pygame.transform.scale(self.surfs[item_name], (60, 60))
                screen.blit(item_image, (box_x + 10, box_y + 10))  # Center inside box
                # check if item is equipped
                if self.game.inventory[item_name]['equipped'] == True:
                    pygame.draw.rect(screen, (255, 215, 0), (box_x, box_y, *self.box_size), 4)

        # draw item description
        if self.selected_index < len(self.inventory_items):
            description_x = self.menu_pos[0] + self.menu_width + 40
            description_y = self.menu_pos[1] + 50
            selected_item = self.inventory_items[self.selected_index]
            description = self.game.inventory[selected_item]['description']
            text = self.game.font.render(description, True, COLORS['white'])
            self.game.render_text(description, COLORS['white'], (description_x, description_y), font_size=15, centered=False)

    def equip_item(self, item_name):
        item_class = ITEMS[item_name]
        scene = self.game.states[-2]
        item = item_class(self.game, scene, [scene.update_sprites, scene.drawn_sprites, scene.obstacle_sprites])
        item.equipped = True
        self.game.inventory[item_name]['equipped'] = True

    def unequip_item(self, item_name):
        # find the equipped item sprite
        item_class = ITEMS[item_name]
        for sprite in self.game.states[-2].update_sprites:
            if isinstance(sprite, item_class):
                sprite.kill()
        self.game.inventory[item_name]['equipped'] = False