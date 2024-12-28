import json
import pygame

from platform import Platform
from spike import Spike

OBSTACLE_TYPES = {
    "platform": Platform,
    "spike": Spike
}

class Level:
    def __init__(self, level_file, screen, assets):
        self.screen = screen
        self.assets = assets
        self.obstacles = []
        self.load_level(level_file)

    def load_level(self, level_file):
        """
        Load level data from a file.
        :param level_file: Path to the level file.
        """
        with open(level_file, 'r') as file:
            data = json.load(file)

        # Load obstacles
        for obstacle in data.get("obstacles", []):
            obstacle_type, x, y , height, width = obstacle["obstacle_type"], obstacle["x"], obstacle["y"], obstacle["height"], obstacle["width"]
            if obstacle["obstacle_type"] in OBSTACLE_TYPES:
                ObstacleClass = OBSTACLE_TYPES[obstacle_type]
                obstacle_obj = ObstacleClass(metadata=obstacle)
                self.obstacles.append(obstacle_obj)

        self.width = data.get("level_width")
        self.height = data.get("level_height")


    def draw(self, camera):
        """
        Draw the level on the screen.
        """
        # Draw level
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, camera)