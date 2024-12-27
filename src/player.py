import pygame

from controls import Controls

class Player:
    def __init__(self, x, y, height, screen, assets):
        """
        Initialize the player object.
        :param x: Initial x-coordinate.
        :param y: Initial y-coordinate.
        :param width: Player width.
        :param height: Player height.
        :param screen: Pygame screen object for rendering.
        :param assets: Dictionary of loaded assets (e.g., images).
        """
        self.x = x
        self.y = y
        self.height = height
        self.screen = screen
        self.assets = assets
        
        # load the player sprite
        self.load_sprites()
        self.sprite = self.sprites["idle_right"][0]
        self.rect = self.sprite.get_rect(topleft=(x, y))

        # movement attributes
        self.gravity = 0.8  # Gravity effect
        self.jump_strength = -15  # Jumping velocity
        self.wall_jump_strength = 3  # Wall jump velocity
        self.speed = 5  # Horizontal movement speed
        self.wall_fall_speed = 2  # Falling speed on a wall
        self.max_fall_speed = 20  # Maximum falling speed
        self.input_ignore_timer = 0 # frames to ignore input after wall jump
        self.vel_x = 0  # Horizontal velocity
        self.vel_y = 0  # Vertical velocity
        self.on_ground = False  # Whether the player is on the ground
        self.on_wall = False  # Whether the player is on a wall
        self.wall_direction = None  # Direction of the wall (left or right)
        self.jumping = False  # Whether the player is jumping
        self.dashing = False  # Whether the player is dashing
        self.in_dash = False  # Whether the player is dashing
        self.dash_timer = 0  # Timer for the dash ability
        self.dash_speed = 15  # Speed of the dash
        self.dash_duration = 10 # Duration of the dash in frames
        self.dash_direction = 0  # Direction of the dash (1 for right, -1 for left)
        self.dash_cooldown = 0 # Cooldown for the dash ability
        self.last_moving = 1  # Last direction the player was moving

        self.current_frame = 0
        self.animation_speed = 100
        self.animation_timer = 0

    def load_sprites(self):
        self.sprites = {
            "idle_right": self.assets["player_idle_right"],
            "idle_left": self.assets["player_idle_left"],
            "right": self.assets["player_right"],
            "left": self.assets["player_left"],
            "jump_right": self.assets["player_jump_right"],
            "jump_left": self.assets["player_jump_left"],
            "wallslide_right": self.assets["player_wallslide_right"],
            "wallslide_left": self.assets["player_wallslide_left"],
            "dash_right": self.assets["player_dash_right"],
            "dash_left": self.assets["player_dash_left"]
        }
        # crop each sprite based on the bounding rect
        for direction in self.sprites:
            for i, sprite in enumerate(self.sprites[direction]):
                bounding_rect = sprite.get_bounding_rect()
                self.sprites[direction][i] = sprite.subsurface(bounding_rect)
                width_height_ratio = self.sprites[direction][i].get_width() / self.sprites[direction][i].get_height()
                self.sprites[direction][i] = pygame.transform.scale(self.sprites[direction][i], (int(self.height * width_height_ratio), self.height))

    def handle_horizontal_collisions(self, platforms):
         self.on_wall = False
         self.wall_direction = None

         for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                    self.on_wall = True
                    self.wall_direction = "right"
                elif self.vel_x < 0:  # Moving left
                    self.rect.left = platform.rect.right
                    self.on_wall = True
                    self.wall_direction = "left"

    def handle_vertical_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    def handle_input(self, keys):
        """
        Handle player input for movement.
        :param keys: List of pressed keys.
        """
        self.vel_x = 0
        if keys[Controls.MOVE_LEFT.value]:  # Move left
            self.vel_x = -self.speed
            self.last_moving = -1
        if keys[Controls.MOVE_RIGHT.value]:  # Move right
            self.vel_x = self.speed
            self.last_moving = 1
        # only jump if the jump key was just pressed (not held)
        if self.jumping == True:
            self.jump()
        # dash if the dash key was just pressed (not held)
        if self.dashing == True:
            self.dash()

    def jump(self):
        if self.on_ground:  # Jump
                self.vel_y = self.jump_strength
        elif self.on_wall: # wall jump
            self.vel_y = self.jump_strength // 1.2
            self.vel_x = self.wall_jump_strength if self.wall_direction == "left" else -self.wall_jump_strength
            self.input_ignore_timer = 10
        self.jumping = False

    def dash(self):
        if not self.in_dash and self.dash_cooldown == 0 and not self.on_wall:
            # start the dash
            self.in_dash = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = 30 # 30 frames cooldown
            if self.vel_x == 0:
                # dash in the direction the player was last moving
                self.dash_direction = self.last_moving
            elif self.vel_x > 0:
                self.dash_direction = 1
            elif self.vel_x < 0:
                self.dash_direction = -1
            self.dashing = False
            #self.sprite = self.sprites["dash"]

    def apply_gravity(self):
        """
        Apply gravity to the player.
        """
        self.vel_y += self.gravity
        if self.on_wall and self.vel_y > self.wall_fall_speed:
            self.vel_y = self.wall_fall_speed
        elif self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed
    
    def reset_position(self):
        """Reset the player to the starting position."""
        self.rect.topleft = (self.x, self.y)
        self.vel_x = 0
        self.vel_y = 0

    def check_out_of_bounds(self, level):
        """Check if the player is out of the level boundaries."""
        offset = 500
        if (self.rect.right < (0-offset) or self.rect.left > (level.width + offset) or
                self.rect.bottom < (0-offset) or self.rect.top > (level.height+offset)):
            self.reset_position()

    def update(self, level, keys):
        """
        Update the player's position and handle collisions.
        :param platforms: List of platform rectangles for collision detection.
        """
        platforms = level.platforms

        self.check_out_of_bounds(level)

        # handle dashing
        if self.in_dash:
            self.dash_timer -= 1
            self.vel_x = self.dash_speed * self.dash_direction
            self.vel_y = 0 # no vertical movement during dash
            if self.dash_timer == 0:
                self.in_dash = False
                self.vel_x = 0

        # handle dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
            # don't reset the dash ability if the player is in the air
            on_ground_or_wall = self.on_ground or self.on_wall
            if self.dash_cooldown == 0 and not on_ground_or_wall:
                self.dash_cooldown = 1

        self.apply_gravity()

        # Update horizontal position
        self.rect.x += self.vel_x

        # Horizontal collision
        self.handle_horizontal_collisions(platforms)

        # Update vertical position
        self.rect.y += self.vel_y

        # Vertical collision
        self.handle_vertical_collisions(platforms)

        # Update the player sprite
        self.update_animation(keys)

    def update_animation(self, keys):
        """
        Update the player sprite based on the movement direction.
        """
        # dashing right
        if self.in_dash and self.dash_direction == 1:
            self.sprite = self.sprites["dash_right"][0]
        # dashing left
        elif self.in_dash and self.dash_direction == -1:
            self.sprite = self.sprites["dash_left"][0]
        # moving right
        elif keys[Controls.MOVE_RIGHT.value] and self.on_ground:
            self.animate("right")
        # moving left
        elif keys[Controls.MOVE_LEFT.value] and self.on_ground:
            self.animate("left")
        # jumping right
        elif not self.on_ground and not self.on_wall and self.last_moving == 1:
            self.sprite = self.sprites["jump_right"][0]
        # jumping left
        elif not self.on_ground and not self.on_wall and self.last_moving == -1:
            self.sprite = self.sprites["jump_left"][0]
        # wall slide right
        elif self.on_wall and not self.on_ground and self.wall_direction == "right":
            self.animate("wallslide_right")
        # wall slide left
        elif self.on_wall and not self.on_ground and self.wall_direction == "left":
            self.animate("wallslide_left")
        # idle right
        elif self.last_moving == 1:
            self.animate("idle_right")
        # idle left
        elif self.last_moving == -1:
            self.animate("idle_left")

    def animate(self, direction):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer >= self.animation_speed:
            self.animation_timer = current_time
            self.current_frame += 1
            if self.current_frame >= len(self.sprites[direction]):
                self.current_frame = 0
            self.sprite = self.sprites[direction][self.current_frame]

    def draw(self, camera):
        """
        Draw the player on the screen.
        """
        self.screen.blit(self.sprite, camera.apply(self.rect))