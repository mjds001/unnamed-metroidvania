from settings import *
from particle import Particle


class PlayerState():
    def __init__(self, character):
        character.frame_index = 0

    def update(self, dt, character):
        character.animate(f'{self.__class__.__name__.lower()}_{character.get_direction()}', 15*dt)
        character.movement()
        character.physics(dt)


class Idle(PlayerState):
    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        
        if INPUTS['left'] or INPUTS['right']:
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
        if character.hit:
            return Hit(character)
        
        if not INPUTS['left'] and not INPUTS['right']:
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
        character.y_forces.append(PLAYER_ATTRIBUTES['jump_force'])
        
    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        if character.on_ground:
            return Idle(character)
        
        if INPUTS['dash']:
            return Dash(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)
        
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)

class WallJump(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        INPUTS['jump'] = False
        self.timer = 0
        # we want to ignore movement inputs briefly after wall jumps
        self.input_delay_duration = 0.2
        self.timer = self.input_delay_duration
        character.y_forces.extend([character.wall_jump_force.y, -character.gravity])
        character.x_forces.append(-character.wall_jump_force.x * character.get_direction(return_int=True))

    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        if character.on_ground:
            return Idle(character)
        
        if INPUTS['dash']:
            return Dash(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)
        
        if character.vel.y > 0 and not character.on_wall and self.timer <= 0:
            return Fall(character)
        
    def update(self, dt, character):
        character.animate(f'jump_{character.get_direction()}', 15*dt)
        if self.timer <= 0:
            character.movement()
        elif self.timer <= self.input_delay_duration/2:
            character.y_forces.extend([character.wall_jump_force.y, -character.gravity])
            character.movement()
        elif self.timer != self.input_delay_duration:
            character.x_forces.append(character.wall_jump_force.x * character.get_direction(return_int=True))
            character.y_forces.extend([character.wall_jump_force.y, -character.gravity])
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
        # allow the player to go faster during dash
        character.max_speed.x = character.max_speed.x * character.dash_mult

    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        if INPUTS['dash']:
            self.dash_pending = True
        if self.timer <= 0:
            if self.dash_pending:
                return Dash(character)
            else:
                character.max_speed.x = character.max_speed.x / character.dash_mult
                return Idle(character)
        # allow player to jump out of dash
        if INPUTS['jump'] and character.on_ground:
            character.max_speed.x = character.max_speed.x / character.dash_mult
            return Jump(character)
        
        if character.on_wall and not character.on_ground:
            character.max_speed.x = character.max_speed.x / character.dash_mult
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
        if character.hit:
            return Hit(character)
        if INPUTS['dash']:
            return Dash(character)
        if character.on_ground:
            return Idle(character)
        if INPUTS['jump']:
            return WallJump(character)
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)
        
    def update(self, dt, character):
        character.y_forces.append(-character.gravity/2) # player should fall slower when on wall
        super().update(dt, character)

class Fall(PlayerState):
    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        if character.on_ground:
            return Idle(character)
        elif character.on_wall:
            return On_Wall(character)
        if INPUTS['dash']:
            return Dash(character)
        
class Hit(PlayerState):
    def __init__(self, character):
        character.invincible_timer = 2
        self.hitstun_timer = 1
        self.create_particles(character)
        super().__init__(character)

    def enter_state(self, character):
        if self.hitstun_timer <= 0:
            character.hit = False
            if character.reset_position == True:
                character.go_to_last_ground_pos()
                return Stun(character)
            return Idle(character)
        
    def create_particles(self, character):
        for n in range(1,10):
            Particle([character.scene.update_sprites, character.scene.drawn_sprites],
                     character.rect.center,
                     direction = -1*character.get_direction(return_int=True),
                     color = (255, 50, 50))
        
    def update(self, dt, character):
        self.hitstun_timer -= dt
        character.animate(f'{self.__class__.__name__.lower()}_{character.get_direction()}', 15*dt)
        character.physics(dt)

class Stun(PlayerState):
    def __init__(self, character):
        self.stun_timer = 1
        super().__init__(character)
    
    def enter_state(self, character):
        if self.stun_timer <= 0:
            return Idle(character)
        
    def update(self, dt, character):
        self.stun_timer -= dt
        character.animate(f'idle_{character.get_direction()}', 15*dt)
        character.physics(dt)

        