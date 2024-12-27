import pygame
import json

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

# Load sprites (using a simple rectangle for now)
platform_sprite = pygame.Surface((GRID_SIZE, GRID_SIZE))
platform_sprite.fill(PLATFORM_COLOR)

# List to hold the placed platforms
platforms = []

# Function to draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLOR, (x, y, GRID_SIZE, GRID_SIZE), 1)

# Function to draw the platforms
def draw_platforms():
    for platform in platforms:
        screen.blit(platform_sprite, platform)

# Function to save the level data
def save_level(filename="level.json"):
    filepath = f"assets/levels/{filename}"
    level_data = {
        "platforms": [{'x': platform[0],
                       'y': platform[1],
                       'height': GRID_SIZE,
                        'width': GRID_SIZE
                        } for platform in platforms],
        "level_width": SCREEN_WIDTH,
        "level_height": SCREEN_HEIGHT
    }
    with open(filepath, 'w') as f:
        json.dump(level_data, f)

# Function to load the level data
def load_level(filename="level.json"):
    global platforms
    platforms = []
    try:
        with open(filename, 'r') as f:
            level_data = json.load(f)
            for platform in level_data:
                platforms.append((platform['x'], platform['y']))
    except FileNotFoundError:
        pass

def handle_input():
    global platforms
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check for mouse click
    if pygame.mouse.get_pressed()[0]:  # Left-click to place a platform
        grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
        grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
        if (grid_x, grid_y) not in platforms:
            platforms.append((grid_x, grid_y))
    
    elif pygame.mouse.get_pressed()[2]:  # Right-click to remove a platform
        grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
        grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
        if (grid_x, grid_y) in platforms:
            platforms.remove((grid_x, grid_y))

# Load the saved level (if any)
load_level()

# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input (mouse clicks)
    handle_input()

    # Draw grid and platforms
    draw_grid()
    draw_platforms()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Save the level when exiting
save_level()

pygame.quit()