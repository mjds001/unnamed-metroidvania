from obstacles.obstacle import Obstacle


class Spike(Obstacle):
    def handle_collisions(self, player):
        """
        Handle collisions with the player.
        """
        player.reset_position()