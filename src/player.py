from pygame.math import Vector2 as vec

from npc import NPC
from settings import *


class Player(NPC):
    def __init__(self, game, scene, groups, pos, name, z='player'):
        super().__init__(game, scene, groups, pos, name, z)
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.3, -self.rect.height*0.2)
        self.move_force = 2600
        self.dash_force = self.move_force * 1.5
        self.jump_force = -20000
        # wall jump force is a vector bc we want the player to jump up and away from the wall
        self.wall_jump_force = vec(self.move_force*0.05, self.jump_force*0.7)
        self.state = Idle(self)

    def collisions(self, axis, group):
        for sprite in self.get_collide_list(group):
            if self.hitbox.colliderect(sprite.hitbox):
                sprite.handle_collisions(axis, self)
        
    def movement(self):
        if INPUTS['left']:
            self.x_forces.append(-self.move_force)
        elif INPUTS['right']:
            self.x_forces.append(self.move_force)
        else:
            self.acc.x = 0

    def exit_scene(self):
        for exit in self.scene.exit_sprites:
            if self.hitbox.colliderect(exit.rect):
                self.scene.new_scene = exit.number
                self.scene.entry_point = self.scene.current_scene
                self.scene.transition.exiting = True

    def update(self, dt):
        self.exit_scene()
        super().update(dt)

class PlayerState():
    def __init__(self, character):
        character.frame_index = 0

    def update(self, dt, character):
        character.animate(f'{self.__class__.__name__.lower()}_{character.get_direction()}', 15*dt)
        character.movement()
        character.physics(dt)


class Idle(PlayerState):
    def enter_state(self, character):
        if abs(character.vel.x) > 1:
            return Run(character)
        
        if INPUTS['dash']:
            return Dash(character)
        
        if INPUTS['jump'] and character.on_ground:
            return Jump(character)
        
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)

class Run(PlayerState):
    def enter_state(self, character):
        if abs(character.vel.x) <= 1:
            return Idle(character)
        
        if INPUTS['dash']:
            return Dash(character)
        
        if INPUTS['jump'] and character.on_ground:
            return Jump(character)
        
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)
        
class Jump(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        INPUTS['jump'] = False
        self.timer = 0
        if character.on_ground:
            character.y_forces.append(character.jump_force)
        elif character.on_wall:
            # we want to ignore movement inputs briefly after wall jumps
            self.input_delay_duration = 2
            self.timer = self.input_delay_duration
            character.y_forces.append(character.wall_jump_force.y)
            character.x_forces.append(-character.wall_jump_force.x * character.get_direction(return_int=True))

    def enter_state(self, character):
        if character.on_ground:
            return Idle(character)
        
        if INPUTS['dash']:
            return Dash(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)
        
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)
        
    def update(self, dt, character):
        character.animate(f'jump_{character.get_direction()}', 15*dt)
        if self.timer <= 0:
            character.movement()
        elif self.timer != self.input_delay_duration:
            character.x_forces.append(character.wall_jump_force.x * 4 * character.get_direction(return_int=True))
        self.timer -= dt
        character.physics(dt)

class Dash(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        INPUTS['dash'] = False
        self.timer = 0.25
        self.dash_pending = False
        # reset the velocity to 0 when the player begins dashing
        character.vel = vec()

    def enter_state(self, character):
        if INPUTS['dash']:
            self.dash_pending = True
        if self.timer <= 0:
            if self.dash_pending:
                return Dash(character)
            else:
                return Idle(character)
        # allow player to jump out of dash
        if INPUTS['jump'] and character.on_ground:
            return Jump(character)
        
        if character.on_wall and not character.on_ground:
            return On_Wall(character)

    def update(self, dt, character):
        self.timer -= dt
        character.animate(f'dash_{character.get_direction()}', 15*dt)
        character.x_forces.append(character.dash_force*character.get_direction(return_int=True))
        # negate the force of gravity so the player will not fall during the dash
        if character.on_ground == False:
            character.y_forces.append(-character.gravity)
        character.physics(dt)

class On_Wall(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        # reset velocity to 0 when player lands on wall
        character.vel = vec()

    def enter_state(self, character):
        if INPUTS['dash']:
            return Dash(character)
        if character.on_ground:
            return Idle(character)
        if INPUTS['jump']:
            return Jump(character)
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)
        
    def update(self, dt, character):
        character.y_forces.append(-character.gravity/2) # player should fall slower when on wall
        super().update(dt, character)

class Fall(PlayerState):
    def enter_state(self, character):
        if character.on_ground:
            return Idle(character)
        elif character.on_wall:
            return On_Wall(character)
        if INPUTS['dash']:
            return Dash(character)
        