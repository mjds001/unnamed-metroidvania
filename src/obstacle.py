import pygame


class Obstacle:
    """
    A generic base class for all obstacles in the game.
    """
    def __init__(self, metadata, sprite):
        """
        metadata may vary depending on the obstacle type.
        At a minimum, metadata should include x, y, width, and height
        """
        x = metadata.get("x")
        y = metadata.get("y")
        width = metadata.get("width")
        height = metadata.get("height")
        self.rect = pygame.Rect(x, y, width, height)
        self.sprite = pygame.transform.scale(sprite, (width, height))

    def draw(self, screen, camera):
        """
        Draws the obstacle on the screen.
        :param screen: The pygame surface to draw on.
        :param camera: The camera object.
        """
        screen.blit(self.sprite, camera.apply(self.rect))

    def colliding(self, player_rect):
        """
        Checks for a collision with the player.
        :param player: The player object.
        :return: True if colliding, False otherwise.
        """
        return self.rect.colliderect(player_rect)
    
    def handle_collisions(self, player):
        """
        Handle collisions with the player.
        :param player: The player object.
        """
        # intentionally left blank to be overridden by subclasses
        pass

    def handle_horizontal_collision(self, player):
        """
        Handle horizontal collisions with the player. By default,
        this method assumes horizontal and vertical collisions are
        handled the same way.
        """
        self.handle_collisions(player)

    def handle_vertical_collision(self, player):
        """
        Handle vertical collisions with the player. By default,
        this method assumes horizontal and vertical collisions are
        handled the same way.
        """
        self.handle_collisions(player)