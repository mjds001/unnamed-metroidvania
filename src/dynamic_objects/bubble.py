from dynamic_objects.dynamic_object import DynamicObject
from settings import *



class Bubble(DynamicObject):
    """
    a class for a floating bubble that will pop after the player jumps off of it.
    The bubble will sink while the player is on it and pop if it hits the ground.
    It will respawn after a set amount of time.
    """

    def __init__(self, game, scene, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z='obstacles', custom_properties = None):
        self.surf = surf
        self.sprite_groups = groups
        super().__init__(game, scene, groups, pos, surf, z, custom_properties)
        self.bounding_rect = self.frames[1].get_bounding_rect()
        self.hitbox = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.bounding_rect.width,
            self.bounding_rect.height
        )
        self.hitbox.bottom = self.rect.bottom
        self.init_pos = pos
        self.fric = OBSTACLE_FRIC
        self.something_on_bubble = False
        self.on_bubble_flag = False
        self.pop_delay = 0
        # add these params to control the bubble floating
        self.vel = vec(0,10)
        self.max_travel = 5
        self.base_y = self.rect.y
        self.precise_pos = vec(self.rect.x, self.rect.y)

    def collisions(self, axis, group):
        if axis == 'x':
            return
        for sprite in self.get_collide_list(group):
            if sprite is self:
                continue
            if self.hitbox.colliderect(sprite.hitbox):
                self.pop()

    def pop(self):
        self.kill()
        new_bubble = {
            'obj_class': Bubble,
            'args': (self.game, self.scene, self.sprite_groups, self.init_pos, self.surf),
            'time_to_spawn': 2
        }
        self.scene.spawn_queue.append(new_bubble)
    
    def handle_collisions(self, axis, character):
        # handle horizontal collisions with a wall
        if axis == 'x':
            if (character.prev_hitbox.right - 1) <= self.hitbox.left <= character.hitbox.right: # character moving right
                character.hitbox.right = self.hitbox.left
            elif (character.prev_hitbox.left + 1) >= self.hitbox.right >= character.hitbox.left: # character moving left
                character.hitbox.left = self.hitbox.right
            elif character.hitbox.left <= self.hitbox.left <= character.hitbox.right:
                character.hitbox.right = self.hitbox.left
            elif character.hitbox.left <= self.hitbox.right <= character.hitbox.right:
                character.hitbox.left = self.hitbox.right
            character.vel.x = 0
            character.rect.centerx = character.hitbox.centerx
        # handle vertical collisions with a wall
        elif axis == 'y':
            if (character.prev_hitbox.bottom - 1) <= self.hitbox.top <= (character.hitbox.bottom): # falling
                self.something_on_bubble = True
                if self.on_bubble_flag == False:
                    self.on_bubble_flag = True
                    self.frame_index += 1
                    self.image = self.frames[self.frame_index]
                character.hitbox.bottom = self.hitbox.top
                # wall applies normal force on character
                # make this force slightly less than gravity so there will still be some downward velocity
                character.y_forces.append(-GRAVITY*character.mass*0.99)
                # add frictional force for walking/running
                character.x_forces.append(self.fric.x * character.vel.x * character.mass)
                character.on_ground = True
            elif (character.prev_hitbox.top + 1) >= self.hitbox.bottom >= character.hitbox.top: # jumping
                character.hitbox.top = self.hitbox.bottom
            character.vel.y = 0
            character.rect.centery = character.hitbox.centery
    
    def physics(self, dt):
        self.collisions('x', self.scene.obstacle_sprites)
        self.collisions('y', self.scene.obstacle_sprites)
        if self.on_bubble_flag == False: # nothing has landed on bubble yet
            # bubble should oscillate if player is not on it
            if self.rect.y > self.base_y + self.max_travel:
                self.vel *= -1
            elif self.rect.y < self.base_y - self.max_travel:
                self.vel *= -1
        if self.something_on_bubble == True:
            # bubble should fall if player is on it
            if self.vel.y < 0:
                self.vel *= -1
            self.pop_delay = 0
            # check if player is still on bubble
            #if not self.scene.player.hitbox.bottom + 3 > self.hitbox.top > self.scene.player.hitbox.bottom - 3:
                #self.pop()
        if self.something_on_bubble == False and self.on_bubble_flag == True:
            if self.pop_delay == 5:
                self.pop()
            else:
                self.pop_delay += 1
        self.precise_pos += self.vel * dt
        self.rect.x = round(self.precise_pos.x)
        self.rect.y = round(self.precise_pos.y)
        self.hitbox.bottomleft = self.rect.bottomleft
        self.something_on_bubble = False
    
    def update(self, dt):
        self.physics(dt)
        
