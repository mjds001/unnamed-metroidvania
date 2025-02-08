from characters.friendly_npc import FriendlyNPC
from dialog_box import DialogBox
from settings import *

import random


class RandomNumberGuy(FriendlyNPC):
    def __init__(self, game, scene, groups, pos, name=None, custom_properties=None, z='entities'):
        self.max_num = 5
        self.number = random.randint(1, self.max_num)
        custom_properties['dialog'] = f'Guess a number between 1 and {self.max_num}.'
        super().__init__(game, scene, groups, pos, name, custom_properties, z)
        self.original_dialog = self.dialog.copy()

    def handle_custom_properties(self, custom_properties):
        super().handle_custom_properties(custom_properties)
        self.dialog.append(DialogBox(self.game, f'Guess', [self.scene.dialog], choices=['1', '2', '3', '4', '5']))

    def handle_inputs(self):
        if INPUTS['up']:
            if self.talking and self.dialog[self.dialog_index].choices:
                choice = self.dialog[self.dialog_index].choices[self.dialog[self.dialog_index].selected_index]
                if choice == str(self.number):
                    self.dialog.append(DialogBox(self.game, f'Correct!', [self.scene.dialog]))
                else:
                    self.dialog.append(DialogBox(self.game, f'Incorrect you idiot!', [self.scene.dialog]))
            self.game.reset_inputs()
            self.progress_dialog()

    def update(self, dt):
        super().update(dt)
        if not self.talking:
            self.dialog = self.original_dialog.copy()