from obstacle import Obstacle
from loaded_assets import obstacle_assets


class Spike(Obstacle):
    def __init__(self, metadata, sprite=obstacle_assets["spike"]):
        """
        metadata is expected to include x, y, width, and height
        """
        super().__init__(metadata, sprite)

    def handle_collisions(self, player):
        """
        Handle collisions with the player.
        """
        player.reset_position()