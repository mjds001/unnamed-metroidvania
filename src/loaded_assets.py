import pygame

obstacle_assets = {
    "platform": pygame.image.load("assets/images/man/block.png"),
    "spike": pygame.image.load("assets/images/man/spikes.png")
}

player_assets = {
    "idle_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0001.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0002.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0003.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0004.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0005.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0006.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0007.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_Idle_0008.png")
    ],
    "idle_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0001.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0002.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0003.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0004.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0005.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0006.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0007.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_Idle_0008.png"), True, False)
    ],
    "run_right": [
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
    "run_left": [
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
    "jump_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0043.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0044.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0045.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0046.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_jump_0047.png")
    ],
    "jump_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0043.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0044.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0045.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0046.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_jump_0047.png"), True, False)
    ],
    "wallslide_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_wallslide0084.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_wallslide0083.png")
    ],
    "wallslide_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_wallslide0084.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_wallslide0083.png"), True, False)
    ],
    "dash_right": [
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0033.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0034.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0035.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0036.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0037.png"),
        pygame.image.load("assets/images/player/Fighter/fighter_dash_0038.png")
    ],
    "dash_left": [
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0033.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0034.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0035.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0036.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0037.png"), True, False),
        pygame.transform.flip(pygame.image.load("assets/images/player/Fighter/fighter_dash_0038.png"), True, False)
    ]
}