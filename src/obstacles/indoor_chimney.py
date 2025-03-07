from obstacles.obstacle import Obstacle
from characters.player_states import Climbing
from settings import *


class IndoorChimney(Obstacle):

    def handle_collisions(self, axis, character):
        # going up chimney
        if character.z == 'player' and character.state.__class__ == Climbing:
            character.climbing = True
            character.rect.centerx = self.rect.centerx
            character.hitbox.center = character.rect.center
            self.z = 'foreground'

    def update(self, dt):
        super().update(dt)
        if self.scene.player.state.__class__ != Climbing:
            self.z = 'obstacles'