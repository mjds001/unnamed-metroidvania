from obstacles.wall import Wall
from settings import *

import pygame
import random


class MovingPlatform(Wall):
    def move(self, obstacles):
        self.rect.x += self.vel * self.direction

        # # check for collisions with obstacles
        # for obstacle in obstacles:
        #     if obstacle is self:
        #         continue
        #     if self.rect.colliderect(obstacle):
        #         self.direction *= -1
        #         self.rect.x += self.vel * self.direction
        #         break

    def handle_horizontal_collision(self, player):
        pass

    def handle_vertical_collision(self, player):
        # the player should move with the platform if colliding
        super().handle_vertical_collision(player)


    def update(self, obstacles):
        self.move(obstacles)