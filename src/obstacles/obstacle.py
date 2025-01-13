import pygame

from settings import TILESIZE

class Obstacle(pygame.sprite.Sprite):
    """
    A generic base class for all obstacles in the game.
    """
    def __init__(self, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='obstacles'):
        """
        metadata may vary depending on the obstacle type.
        At a minimum, metadata should include x, y, width, and height
        """
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(0,0)
        self.z = z

    def draw(self, screen, camera):
        """
        Draws the obstacle on the screen.
        :param screen: The pygame surface to draw on.
        :param camera: The camera object.
        """
        screen.blit(self.image, camera.apply(self.rect))

    def colliding(self, player_rect):
        """
        Checks for a collision with the player.
        :param player: The player object.
        :return: True if colliding, False otherwise.
        """
        return self.rect.colliderect(player_rect)
    
    def handle_collisions(self, axis, character):
        """
        Handle collisions with the player.
        :param player: The player object.
        """
        # intentionally left blank to be overridden by subclasses
        pass

    def update(self, obstacles):
        """
        to be filled in for sub classes that require updates
        eg. moving platforms
        """
        pass