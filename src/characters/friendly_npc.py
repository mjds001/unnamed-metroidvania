"""
A class for friendly NPCs that the player can interact with
"""

from characters.npc import NPC
from dialog.dialog_box import DialogBox
from dialog.dialog_cue import DialogCue
from characters.player_states import Talking, Idle
from settings import *



class FriendlyNPC(NPC):
    def __init__(self, game, scene, groups, pos, name=None, custom_properties=None, z='entities'):
        self.has_dialog = False # default to false, update to true when handling custom properties
        super().__init__(game, scene, groups, pos, name, custom_properties, z)

    def handle_custom_properties(self, custom_properties):
        if 'dialog' in custom_properties:
            self.has_dialog = True
            text = custom_properties['dialog']
            # dialog slides are broken up by /n characters in the text
            text = text.split('/n')
            self.dialog = []
            for text_slide in text:
                self.dialog.append(DialogBox(self.game, text_slide, [self.scene.dialog]))
            self.dialog_index = 0
            self.dialog_cue = DialogCue(self.game, 'Press UP to talk', [self.scene.dialog])

    def get_distance_to_player(self):
        return ((self.hitbox.centerx - self.scene.player.hitbox.centerx)**2 + (self.hitbox.centery - self.scene.player.hitbox.centery)**2)**0.5
    
    def handle_inputs(self):
        if INPUTS['up']:
            self.game.reset_inputs()
            self.progress_dialog()
    
    def update(self, dt):
        super().update(dt)
        if self.has_dialog:
            # check if the player is nearby
            if self.get_distance_to_player() < 40:
                if not self.talking:
                    self.dialog_cue.show()
                self.handle_inputs()
            else:
                self.dialog_cue.hide()

    def progress_dialog(self):
        # if no dialog is being shown, show the first slide
        if not self.talking:
            self.talking = True
            self.scene.player.change_state(Talking(self.scene.player))
            self.dialog[self.dialog_index].show()
            self.dialog_cue.hide()
        # if dialog is being shown but has not been fully shown, show the full dialog
        elif not self.dialog[self.dialog_index].full_dialog_shown:
            self.dialog[self.dialog_index].show_full_dialog()
        # if the dialog is fully shown, hide it and move to the next slide
        elif self.dialog[self.dialog_index].full_dialog_shown:
            self.dialog[self.dialog_index].hide()
            self.dialog_index += 1
            # if there are no more slides, reset the dialog
            if self.dialog_index >= len(self.dialog):
                self.dialog_index = 0
                self.talking = False
                self.scene.player.talking = False
                self.dialog_cue.show()
            else:
                self.dialog[self.dialog_index].show()