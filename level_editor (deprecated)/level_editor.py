import pygame
import json


class LevelEditor:
    """
    Class to define a UI for creating levels.
    """
    def __init__(self, screen, grid_size, grid_color, assets):
        self.screen = screen
        self.grid_size = grid_size
        self.grid_color = grid_color
        self.assets = assets
        self.obstacle_sprites = {
            tool: pygame.transform.scale(info["sprite"], (info["width"], info["height"]))
            for tool, info in assets.items()
        }
        self.level_data = []
        self.selected_tool = "platform" # default tool
        self.font = pygame.font.Font(None, 36)

        # toolbar setup
        self.toolbar_items = list(self.obstacle_sprites.keys())
        self.toolbar_icons = {
            item: pygame.transform.scale(self.obstacle_sprites[item], (grid_size, grid_size))
            for item in self.toolbar_items
            }
        self.toolbar_rects = self.create_toolbar_rects()

    def create_toolbar_rects(self):
        """
        Create the toolbar rectangles.
        """
        toolbar_rects = {}
        x, y = 10, 10 # starting position of the toolbar
        for tool in self.toolbar_items:
            toolbar_rects[tool] = pygame.Rect(x, y, 50, 50)
            x += 60 # space between icons
        return toolbar_rects
    
    def draw_toolbar(self):
        """
        Draw the toolbar.
        """
        for tool, rect in self.toolbar_rects.items():
            # highlight the selected tool
            if tool == self.selected_tool:
                pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(5, 5))

            # draw the icon
            self.screen.blit(self.toolbar_icons[tool], rect.topleft)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

    def draw_grid(self):
        """
        Draw the grid on the screen.
        """
        for x in range(0, self.screen.get_width(), self.grid_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.screen.get_height()))
        for y in range(0, self.screen.get_height(), self.grid_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.screen.get_width(), y))

    def handle_toolbar_click(self, mouse_pos):
        """
        Handle toolbar click events.
        """
        for tool, rect in self.toolbar_rects.items():
            if rect.collidepoint(mouse_pos):
                self.selected_tool = tool
                return

    def place_obstacle(self, pos):
        """
        Place an obstacle at the given position.
        """
        grid_x = (pos[0] // self.grid_size) * self.grid_size
        grid_y = (pos[1] // self.grid_size) * self.grid_size
        if any(obstacle["x"] == grid_x and obstacle["y"] == grid_y for obstacle in self.level_data):
            return
        
        obstacle = {
            "obstacle_type": self.selected_tool,
            "x": grid_x,
            "y": grid_y,
            "height": self.assets[self.selected_tool]["height"],
            "width": self.assets[self.selected_tool]["width"]
        }
        if self.selected_tool == "moving_platform":
            obstacle['waypoints'] = [(grid_x - obstacle['width']*2.5//1, grid_y + obstacle['height']//2),
                                     (grid_x + obstacle['width']*3.5//1, grid_y + obstacle['height']//2)]
        self.level_data.append(obstacle)

    def remove_obstacle(self, pos):
        """
        Remove an obstacle at the given position.
        """
        grid_x = (pos[0] // self.grid_size) * self.grid_size
        grid_y = (pos[1] // self.grid_size) * self.grid_size
        self.level_data = [obstacle for obstacle in self.level_data if obstacle["x"] != grid_x or obstacle["y"] != grid_y]

    def render_obstacles(self):
        """
        Render the obstacles on the screen.
        """
        for obstacle in self.level_data:
            self.screen.blit(self.obstacle_sprites[obstacle["obstacle_type"]], (obstacle["x"], obstacle["y"]))
            if obstacle["obstacle_type"] == "moving_platform":
                # also render the waypoints for the platform
                for wx, wy in obstacle["waypoints"]:
                    pygame.draw.circle(self.screen, (255, 0, 0), (wx, wy), 5)
                pygame.draw.lines(self.screen, (0,255,0), True, obstacle["waypoints"], 2)

    def handle_inputs(self):
        """
        Handle inputs for the level editor.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if any(rect.collidepoint(mouse_x, mouse_y) for rect in self.toolbar_rects.values()):
                self.handle_toolbar_click((mouse_x, mouse_y))
            else:
                self.place_obstacle((mouse_x, mouse_y))

        if pygame.mouse.get_pressed()[2]:
            self.remove_obstacle((mouse_x, mouse_y))

    def save_level(self, filename="level.json"):
        """
        Save the level data to a JSON file.
        """
        filepath = f"assets/levels/{filename}"
        level_data = {
            "obstacles": self.level_data,
            "level_width": self.screen.get_width(),
            "level_height": self.screen.get_height()
        }
        with open(filepath, 'w') as f:
            json.dump(level_data, f, indent=4)

    def load_level(self, filename="level.json"):
        """
        Load the level data from a JSON file.
        """
        filepath = f"assets/levels/{filename}"
        try:
            with open(filepath, 'r') as f:
                level_data = json.load(f)
                self.level_data = level_data["obstacles"]
        except FileNotFoundError:
            pass
