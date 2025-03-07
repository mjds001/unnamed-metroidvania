"""
A class for signs that the player can interact with to read
This seems like more of an "obstacle" than an "entity", but the interaction behavior better
fits with the friendly_npc class.
"""

from characters.friendly_npc import FriendlyNPC
from dialog.dialog_cue import DialogCue
from settings import *


class Sign(FriendlyNPC):
    def handle_custom_properties(self, custom_properties):
        super().handle_custom_properties(custom_properties)
        self.dialog_cue = DialogCue(self.game, 'Press UP to read', [self.scene.dialog])