from pygame.math import Vector2 as vec

from characters.npc import NPC
from settings import *
from appendix import *
from characters.player_states import *


class Player(NPC):
    def __init__(self, game, scene, groups, pos, name, custom_properties=None, z='player'):
        super().__init__(game, scene, groups, pos, name, custom_properties, z)
        if self.name == 'ninja':
            self.hitbox = self.rect.copy().inflate(-self.rect.width*0.7, -self.rect.height*0.2)
        if self.name == 'santa_merry':
            self.hitbox = self.rect.copy().inflate(-self.rect.width*0.6, -self.rect.height*0.05)
        self.equip_items()
        
        self.ground_move_force = 3300
        self.air_move_force = self.ground_move_force*0.5
        self.max_speed = vec(2.63, 7.5)
        self.dash_mult = 1.5
        self.max_dash_speed = self.max_speed.x * self.dash_mult
        self.dash_force = self.ground_move_force * self.dash_mult
        self.jump_force = -22000
        # wall jump force is a vector bc we want the player to jump up and away from the wall
        self.wall_jump_force = vec(self.air_move_force*0.8, -self.air_move_force*0.8)
        self.state = Idle(self)

    def equip_items(self):
        """
        when entering a new room, initialize the player with the items they
        had equipped in the previous room
        """
        for item, info in self.game.inventory.items():
            if info['equipped'] == True:
                item_class = ITEMS[item]
                item_obj = item_class(self.game, self.scene,
                                      [self.scene.update_sprites, self.scene.drawn_sprites, self.scene.obstacle_sprites])
                item_obj.equipped = True

    def collisions(self, axis, group):
        for sprite in self.get_collide_list(group):
            if self.hitbox.colliderect(sprite.hitbox):
                sprite.handle_collisions(axis, self)
        
    def movement(self):
        if INPUTS['left']:
            if self.on_ground:
                self.x_forces.append(-self.ground_move_force)
            else:
                self.x_forces.append(-self.air_move_force)
        elif INPUTS['right']:
            if self.on_ground:
                self.x_forces.append(self.ground_move_force)
            else:
                self.x_forces.append(self.air_move_force)
        else:
            self.acc.x = 0

    def progress_dialog(self, dialog, dialog_index):
        # if no dialog is being shown, show the first slide
        if not self.talking:
            self.talking = True
            self.change_state(Talking(self))
            dialog[dialog_index].show()
        # if dialog is being shown but has not been fully shown, show the full dialog
        elif not dialog[dialog_index].full_dialog_shown:
            dialog[dialog_index].show_full_dialog()
        # if the dialog is fully shown, hide it and move to the next slide
        elif dialog[dialog_index].full_dialog_shown:
            dialog[dialog_index].hide()
            dialog_index += 1
            # if there are no more slides, reset the dialog
            if dialog_index >= len(dialog):
                dialog_index = 0
                self.talking = False
            else:
                dialog[dialog_index].show()
        return dialog_index

    def go_to_last_ground_pos(self):
        self.hitbox.center = self.last_on_ground_pos
        self.rect.center = self.hitbox.center
        self.vel = vec()
        self.acc = vec()

    def go_to_entrypoint(self):
        self.hitbox.topleft = self.entrypoint
        self.rect.center = self.hitbox.center
        self.vel = vec()
        self.acc = vec()

    def exit_scene(self):
        for exit in self.scene.exit_sprites:
            if self.hitbox.colliderect(exit.rect):
                self.scene.new_scene = exit.number
                self.scene.entry_point = self.scene.current_scene
                self.scene.transition.exiting = True

    def change_state(self, new_state=None):
        # if a new state is passed, use that state
        if new_state:
            self.state = new_state
        # if no new state is passed, check if the current state has changed
        else:
            new_state = self.state.enter_state(self)
            # verify that the new state is in the list of states for this character name
            if new_state and new_state.__class__.__name__.lower() in PLAYER_STATE_INDEX[self.name]:
                self.state = new_state
            else:
                self.state

    def update(self, dt):
        self.exit_scene()
        if self.invincible_timer >= 0:
            self.invincible_timer -= dt
        super().update(dt)