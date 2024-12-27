class Camera:
    def __init__(self, screen_width, screen_height, level_width, level_height, box_margin):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_width = level_width
        self.level_height = level_height
        self.box_margin = box_margin

        # Camera's position in the game world
        self.camera_x = 0
        self.camera_y = 0

    def update(self, player_rect):
        # Define the safe zone (box)
        box_left = self.camera_x + self.box_margin
        box_right = self.camera_x + self.screen_width - self.box_margin
        box_top = self.camera_y + self.box_margin
        box_bottom = self.camera_y + self.screen_height - self.box_margin

        # Move the camera if the player goes outside the box
        if player_rect.left < box_left:
            self.camera_x -= box_left - player_rect.left
        if player_rect.right > box_right:
            self.camera_x += player_rect.right - box_right
        if player_rect.top < box_top:
            self.camera_y -= box_top - player_rect.top
        if player_rect.bottom > box_bottom:
            self.camera_y += player_rect.bottom - box_bottom

        # Clamp the camera position to the level boundaries
        self.camera_x = max(0, min(self.camera_x, self.level_width - self.screen_width))
        self.camera_y = max(0, min(self.camera_y, self.level_height - self.screen_height))

    def apply(self, rect):
        # Offset a rect by the camera's position
        return rect.move(-self.camera_x, -self.camera_y)