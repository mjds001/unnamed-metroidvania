import pygame
import json

from level_editor import LevelEditor

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
GRID_SIZE = 25  # Size of the grid squares
GRID_COLOR = (200, 200, 200)  # Color of grid lines
BACKGROUND_COLOR = (255, 255, 255)  # Background color
PLATFORM_COLOR = (0, 255, 0)  # Platform color

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level Editor")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load sprites
assets = {
    "platform": {
        "sprite": pygame.image.load("assets/images/man/block.png"),
        "width": GRID_SIZE,
        "height": GRID_SIZE
    },
    "spike": {
        "sprite": pygame.image.load("assets/images/man/spikes.png"),
        "width": GRID_SIZE,
        "height": GRID_SIZE
    },
    "moving_platform": {
        "sprite": pygame.image.load("assets/images/man/block-filled.png"),
        "width": GRID_SIZE*4,
        "height": GRID_SIZE/3
    }
}


level_editor = LevelEditor(screen, GRID_SIZE, GRID_COLOR, assets)


# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    level_editor.draw_toolbar() # Draw the toolbar
    level_editor.draw_grid() # Draw the grid
    level_editor.render_obstacles() # Draw the obstacles
    level_editor.handle_inputs() # Handle inputs

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Save the level when exiting
level_editor.save_level()

pygame.quit()