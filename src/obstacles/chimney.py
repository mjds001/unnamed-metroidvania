from obstacles.wall import Wall
from settings import *
from characters.player_states import Climbing



class Chimney(Wall):
    """
    Chimney will act kind of like a pipe in mario- player can press down when standing on
    a chimney to travel somewhere
    """
    def __init__(self, scene, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='foreground', tile = None):
        super().__init__(scene, groups, pos, surf, z, tile)
        self.bounding_rect = self.image.get_bounding_rect()
        self.hitbox = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.bounding_rect.width,
            self.bounding_rect.height
        )
        self.hitbox.bottom = self.rect.bottom

    def handle_collisions(self, axis, character):
        if character.z != 'player':
            super().handle_collisions(axis, character)
            return
        if character.z == 'player':
            if character.state.__class__ != Climbing:
                super().handle_collisions(axis, character)
            # going down chimney
            if INPUTS['down']:
                character.climbing = True
                if character.state.__class__!= Climbing:
                    character.change_state(Climbing(character))
                elif character.state.__class__ == Climbing:
                    character.climbing = True
                character.rect.y += 1
                character.rect.centerx = self.rect.centerx
                character.hitbox.center = character.rect.center
        
