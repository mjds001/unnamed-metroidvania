from obstacles.obstacle import Obstacle
from obstacles.wall import Wall
from settings import *



class Button(Wall):

    def __init__(self, groups, pos, surf, z='obstacles'):
        # the surf passed in will contain image for button pressed and unpressed
        self.frames = surf
        surf = self.frames[0]
        super().__init__(groups, pos, surf, z)
        self.bounding_rect = self.frames[1].get_bounding_rect()
        self.hitbox = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.bounding_rect.width,
            self.bounding_rect.height
        )
        self.hitbox.bottom = self.rect.bottom
        self.pressed = False

    def handle_collisions(self, axis, character):
        self.pressed = True
        self.image = self.frames[1]
        super().handle_collisions(axis, character)

    def update(self, dt):
        if not self.pressed:
            self.image = self.frames[0]
        self.pressed = False