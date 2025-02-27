from obstacles.wall import Wall
from settings import *


class Ice(Wall):
    """
    it's like a wall, but slippery
    """

    def __init__(self, groups, pos, surf, z='obstacles', tile = None):
        super().__init__(groups, pos, surf, z, tile)
        self.fric = vec(-1,-1)