import pygame
from level import Level
from player import Player
from camera import Camera
from controls import Controls

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load assets
assets = {
    "platform": pygame.image.load("assets/images/wall/brick.png"),
    "player_idle_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0001.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0002.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0003.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0004.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0005.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0006.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0007.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0008.png")
    ],
    "player_idle_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0001.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0002.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0003.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0004.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0005.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0006.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0007.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0008.png"), True, False)
    ],
    "player_right": [
        #pygame.image.load("assets/images/man/man-run1.png"),
        #pygame.image.load("assets/images/man/man-run2.png"),
        #pygame.image.load("assets/images/man/man-run3.png")
        pygame.image.load("assets/images/player/Fighter/fighter_run_0022.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_run_0023.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_run_0024.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_run_0017.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_run_0018.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_run_0019.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_run_0020.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_run_0021.png")
    ],
    # for left movement, flip the images
    "player_left": [
        #pygame.transform.flip(pygame.image.load("assets/images/man/man-run1.png"), True, False),
        #pygame.transform.flip(pygame.image.load("assets/images/man/man-run2.png"), True, False),
        #pygame.transform.flip(pygame.image.load("assets/images/man/man-run3.png"), True, False)
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0022.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0023.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0024.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0017.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0018.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0019.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0020.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_run_0021.png"), True, False)
    ],
    "player_jump_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0043.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0044.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0045.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0046.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0047.png")
    ],
    "player_jump_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0043.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0044.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0045.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0046.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0047.png"), True, False)
    ],
    "player_wallslide_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_wallslide0084.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_wallslide0083.png")
    ],
    "player_wallslide_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_wallslide0084.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_wallslide0083.png"), True, False)
    ],
    "player_dash_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0033.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0034.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0035.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0036.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0037.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0038.png")
    ],
    "player_dash_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0033.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0034.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0035.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0036.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0037.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0038.png"), True, False)
    ]
}

# Load the level
level = Level("assets/levels/level.json", screen, assets)

# Create the player
player = Player(x=100, y=450, height=50, screen=screen, assets=assets)

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
            if event.key == Controls.DASH.value:
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