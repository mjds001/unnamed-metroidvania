
from settings import *
from obstacles.obstacle import Obstacle
from characters.player_states import Climbing

class Ladder(Obstacle):
    """
    A class for ladders that the player can climb
    """

    def __init__(self, scene, groups, pos, surf=None, z='obstacles', tile = None):
        super().__init__(scene, groups, pos, surf, z, tile)
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.6,0)

    def handle_collisions(self, axis, character):
        if character.z != 'player':
            return
        if axis == 'x':
            return
        if INPUTS['up'] and character.vel.y > 0:
            character.climbing = True
            if character.state.__class__.__name__ != Climbing.__name__:
                character.change_state(Climbing(character))
        elif character.state.__class__.__name__ == Climbing.__name__:
            character.climbing = True
        
