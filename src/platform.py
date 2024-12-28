from obstacle import Obstacle
from loaded_assets import obstacle_assets

class Platform(Obstacle):
    def __init__(self, metadata, sprite=obstacle_assets["platform"]):
        """
        metadata is expected to include x, y, width, and height
        """
        super().__init__(metadata, sprite)

    def handle_horizontal_collision(self, player):
        """
        Handle horizontal collisions with the player.
        """
        if player.vel_x > 0: # moving right
            player.rect.right = self.rect.left
            player.on_wall = True
            player.wall_direction = "right"
        elif player.vel_x < 0: # moving left
            player.rect.left = self.rect.right
            player.on_wall = True
            player.wall_direction = "left"
        player.vel_x = 0

    def handle_vertical_collision(self, player):
        """
        Handle vertical collisions with the player.
        """
        if player.vel_y > 0: # falling
            player.rect.bottom = self.rect.top
            player.on_ground = True
        elif player.vel_y < 0: # jumping
            player.rect.top = self.rect.bottom
        player.vel_y = 0