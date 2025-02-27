from settings import *
from particles.hit_particle import HitParticle
from particles.snowball import Snowball
from particles.particle import Particle
from states.dead import Dead

import random

# index to track which character names are able to enter certain states
PLAYER_STATE_INDEX = {
    'ninja': ['idle', 'run', 'jump', 'fall', 'hit', 'stun', 'on_wall', 'wall_jump', 'dash', 'talking'],
    'santa_merry': ['idle', 'run', 'jump', 'fall', 'hit', 'stun', 'talking', 'climbing', 'throw', 'crush', 'push'],
}


class PlayerState():
    def __init__(self, character):
        # verify that this state is in the list of states for this character name
        if self.__class__.__name__.lower() not in PLAYER_STATE_INDEX[character.name]:
            # exit out of this init and the init of any subclasses by saving an invalid state flag
            self.invalid_state = True
            return
        self.invalid_state = False
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
        
        if INPUTS['throw']:
            return Throw(character)
        
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)

class Run(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return

    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        
        if not INPUTS['left'] and not INPUTS['right']:
            return Idle(character)
        
        if INPUTS['dash']:
            return Dash(character)
        
        if INPUTS['throw']:
            return Throw(character)
        
        if INPUTS['jump'] and character.on_ground:
            return Jump(character)
        
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)
        
    def update(self, dt, character):
        super().update(dt, character)
        
class Jump(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
        INPUTS['jump'] = False
        character.y_forces.append(character.jump_force)
        
    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        if character.on_ground:
            return Idle(character)
        
        if INPUTS['dash']:
            return Dash(character)
        
        if INPUTS['throw']:
            return Throw(character)
        
        if character.on_wall and not character.on_ground and character.vel.y >= 0:
            return On_Wall(character)
        
        if character.vel.y > 0 and not character.on_wall:
            return Fall(character)

class WallJump(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
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
        if self.invalid_state:
            return
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
        if self.invalid_state:
            return
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
        if INPUTS['throw']:
            return Throw(character)
        
class Hit(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
        character.invincible_timer = 2
        self.hitstun_timer = 1
        self.create_particles(character)

    def enter_state(self, character):
        if self.hitstun_timer <= 0:
            character.hit = False
            if character.reset_position == True:
                character.go_to_last_ground_pos()
                return Stun(character)
            return Idle(character)
        
    def create_particles(self, character):
        for n in range(1,10):
            HitParticle([character.scene.update_sprites, character.scene.drawn_sprites],
                     character.rect.center,
                     direction = -1*character.get_direction(return_int=True),
                     color = (255, 50, 50))
        
    def update(self, dt, character):
        self.hitstun_timer -= dt
        character.animate(f'{self.__class__.__name__.lower()}_{character.get_direction()}', 15*dt)
        character.physics(dt)

class Stun(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
        character.invincible_timer = 1
        self.stun_timer = 1
    
    def enter_state(self, character):
        if self.stun_timer <= 0:
            return Idle(character)
        
    def update(self, dt, character):
        self.stun_timer -= dt
        character.animate(f'idle_{character.get_direction()}', 15*dt)
        character.physics(dt)

class Talking(PlayerState):
    """
    if a player is talking, they should not move or enter any other state until the dialog is finished
    """
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
        character.talking = True
        # reset the player velocity to 0 when they start talking
        character.vel = vec()
        character.acc = vec()
        character.x_forces = []
        character.y_forces = []
        character.invincible_timer = 1
        
    def enter_state(self, character):
        if not character.talking:
            character.invincible_timer = 0
            return Idle(character)
        
    def update(self, dt, character):
        # character should remain invincible while talking
        character.invincible_timer = 1
        character.animate(f'talking_{character.get_direction()}', 15*dt)
        character.physics(dt)

class Climbing(PlayerState):
    """
    a state for when the player is climbing a ladder
    """
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
        # reset the player velocity to 0 when they start climbing
        character.vel = vec()
        character.acc = vec()
        character.x_forces = []
        character.y_forces = []
        self.just_started_climbing = True

    def enter_state(self, character):
        if character.hit:
            return Hit(character)
        if INPUTS['dash']:
            return Dash(character)
        if not character.climbing:
            return Idle(character)
        if INPUTS['jump']:
            character.vel = vec()
            return Jump(character)
        if character.on_ground and not self.just_started_climbing:
            return Idle(character)
        if self.just_started_climbing:
            self.just_started_climbing = False
        
    def update(self, dt, character):
        character.vel.y = 0
        character.vel.x = 0
        if INPUTS['up']:
            character.vel.y = -character.max_speed[0]
        elif INPUTS['down']:
            character.vel.y = character.max_speed[0]
        # negate the force of gravity
        character.y_forces.append(-character.gravity * character.mass)

        if INPUTS['up'] or INPUTS['down']:
            character.animate(f'{self.__class__.__name__.lower()}_{character.get_direction()}', 15*dt)
        character.movement()
        character.physics(dt)
        
class Throw(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
        INPUTS['throw'] = False
        self.create_snowball(character)

    def create_snowball(self, character):
        Snowball([character.scene.update_sprites, character.scene.drawn_sprites],
                    character.rect.center,
                    direction = character.get_direction(return_int=True)
                    )

    def enter_state(self, character):
        if character.frame_index == len(character.animations[f'{self.__class__.__name__.lower()}_{character.get_direction()}']) - 1:
            return Idle(character)
        
class Crush(PlayerState):
    def __init__(self, character):
        super().__init__(character)
        if self.invalid_state:
            return
        self.rect_bottomleft = character.hitbox.bottomleft
        
    def enter_state(self, character):
        if character.frame_index == len(character.animations[f'{self.__class__.__name__.lower()}_{character.get_direction()}']) - 1:
            self.create_particles(character)
            character.kill()
            Dead(character.game).enter_state()
            character.game.reset_inputs()
        
    def create_particles(self, character):
        for n in range(1,10):
            Particle(groups= [character.scene.update_sprites, character.scene.drawn_sprites],
                        pos= character.rect.center,
                        vel= vec(random.uniform(-200,200), random.uniform(-200,0)),
                        size= random.randint(4,6),
                        color= COLORS['red']
                        )
        
    def update(self, dt, character):
        character.animate(f'{self.__class__.__name__.lower()}_{character.get_direction()}', 15*dt)
        image_rect = character.image.get_rect()
        character.hitbox = image_rect.copy()
        character.hitbox.bottomleft = self.rect_bottomleft
        character.rect = character.hitbox.copy()

class Push(Run):
    def __init__(self, character):
        super().__init__(character)