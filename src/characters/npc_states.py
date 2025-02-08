

class Idle():
    def enter_state(self, character):
        if abs(character.vel.x) > 1:
            return Run()

    def update(self, dt, character):
        character.animate(f'idle_{character.get_direction()}', 15*dt)
        character.movement()
        character.physics(dt)

class Run:
    def enter_state(self, character):
        if abs(character.vel.x) <= 1:
            return Idle()
        
    def update(self, dt, character):
        character.animate(f'run_{character.get_direction()}', 15*dt)
        character.movement()
        character.physics(dt)
