import pygame

from level import Level
from player import Player
from camera import Camera
from controls import Controls
from loaded_assets import player_assets, obstacle_assets

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load assets


# Load the level
level = Level("assets/levels/level.json", screen, obstacle_assets)

# Create the player
player = Player(x=100, y=450, height=50, screen=screen, sprites=player_assets)

# Create the camera
camera = Camera(
    screen_width= screen_width,          # Width of the visible game area
    screen_height= screen_height,         # Height of the visible game area
    level_width=level.width,          # Width of the entire level
    level_height=level.height,         # Height of the entire level
    box_margin=250             # Margin around the safe zone
)
level.draw(camera)

# Main game loop
running = True
while running:
    # event handling
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == Controls.JUMP.value:
                player.jumping = True
            if event.key == Controls.DASH.value and player.dash_cooldown == 0:
                player.dashing = True
        
    # Update the player
    if player.input_ignore_timer == 0:
        player.handle_input(keys)
    else:
        player.input_ignore_timer -= 1
    player.update(level, keys)
    camera.update(player.rect)
    

    # Draw everything
    screen.fill((135, 206, 235))  # Clear the screen
    level.draw(camera)            # Draw the level
    player.draw(camera)           # Draw the player
    pygame.display.flip()   # Update the display
    clock.tick(60)          # Cap the frame rate

pygame.quit()