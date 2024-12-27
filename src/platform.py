import pygame

class Platform:
    def __init__(self, x, y, width, height, assets):
        """
        Initializes a platform.
        :param x: X position of the platform.
        :param y: Y position of the platform.
        :param width: Width of the platform.
        :param height: Height of the platform.
        """
        self.sprite = assets["platform"]
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        """
        Draws the platform on the screen.
        :param screen: The pygame surface to draw on.
        """
        screen.blit(self.sprite, self.rect.topleft)

    def collide(self, player_rect):
        """
        Checks for a collision with the player.
        :param player_rect: The player's collision rectangle.
        :return: True if colliding, False otherwise.
        """
        return self.rect.colliderect(player_rect)