from obstacles.obstacle import Obstacle
from settings import *



class Button(Obstacle):

    def __init__(self, groups, pos, surf, z='obstacles'):
        # the surf passed in will contain image for button pressed and unpressed
        self.frames = surf
        surf = self.frames[0]
        super().__init__(groups, pos, surf, z)                                                                                                                                             

    def handle_collisions(self, axis, character):
        self.image = self.frames[1]