import json
import pygame

from platform import Platform


class Level:
    def __init__(self, level_file, screen, assets):
        self.screen = screen
        self.assets = assets
        self.platforms = []
        self.load_level(level_file)

    def load_level(self, level_file):
        """
        Load level data from a file.
        :param level_file: Path to the level file.
        """
        with open(level_file, 'r') as file:
            data = json.load(file)

        # Load platforms
        for platform_data in data.get("platforms", []):
            x, y , height, width = platform_data["x"], platform_data["y"], platform_data["height"], platform_data["width"]
            platform = Platform(x, y, height, width, self.assets)
            self.platforms.append(platform)

        self.width = data.get("level_width")
        self.height = data.get("level_height")


    def draw(self, camera):
        """
        Draw the level on the screen.
        """
        # Draw platforms
        for platform in self.platforms:
            self.screen.blit(platform.sprite, camera.apply(platform.rect))