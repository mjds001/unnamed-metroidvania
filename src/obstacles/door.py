from obstacles.wall import Wall
from settings import *
from dialog.dialog_box import DialogBox
from dialog.dialog_cue import DialogCue
from characters.player_states import Talking

import pygame


class Door(Wall):
    def __init__(self, scene, groups, pos, surf=None, z='obstacles', tile=None):
        super().__init__(scene, groups, pos, surf,z)
        self.bounding_rect = self.image.get_bounding_rect()
        self.true_hitbox = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.bounding_rect.width,
            self.bounding_rect.height
        )
        self.open = False
        self.talking = False
        self.dialog = []
        self.dialog_index = 0
        self.dialog_cues = []
        self.dialog_cue_index = 0
        self.dialog.append(DialogBox(self.scene.game, 'Am I really about to walk out the front door like some common idiot? I dont think so.', self.scene.dialog))
        self.dialog_cues.append(DialogCue(self.scene.game, f'Press {pygame.key.name(Controls.INTERACT.value)} to open', self.scene.dialog))
        self.dialog_cues.append(DialogCue(self.scene.game, f'Press {pygame.key.name(Controls.INTERACT.value)} to close', self.scene.dialog))

    def handle_collisions(self, axis, character):
        if character.z == 'player':
            if INPUTS[pygame.key.name(Controls.INTERACT.value)] == True and character.state.__class__ != Talking:
                if self.open == False:
                    self.open = True
                    self.image = self.frames[1]
                    self.dialog_cue_index = 1
                elif self.open == True:
                    self.open = False
                    self.image = self.frames[0]
                    self.dialog_cue_index = 0
                self.scene.game.reset_inputs()
        
            if self.open == True and character.hitbox.colliderect(self.true_hitbox) and self.talking == False:
                self.talking = True
                self.dialog_index = character.progress_dialog(self.dialog, self.dialog_index)
            elif self.talking == True and INPUTS[pygame.key.name(Controls.INTERACT.value)] == True:
                self.scene.game.reset_inputs()
                self.dialog_index = character.progress_dialog(self.dialog, self.dialog_index)
                if character.talking == False: # dialog concluded
                    self.talking = False
                    character.x_forces.append(40000)
                    self.open = False
                    self.image = self.frames[0]
                    self.dialog_cue_index = 0

        if character.hitbox.colliderect(self.true_hitbox):
            self.handle_true_collisions(axis, character)

    def handle_true_collisions(self, axis, character):
        # handle horizontal collisions with a wall
        if axis == 'x':
            if (character.prev_hitbox.right - 1) <= self.true_hitbox.left <= character.hitbox.right: # character moving right
                character.hitbox.right = self.true_hitbox.left
            elif (character.prev_hitbox.left + 1) >= self.true_hitbox.right >= character.hitbox.left: # character moving left
                character.hitbox.left = self.true_hitbox.right
            elif character.hitbox.left <= self.true_hitbox.left <= character.hitbox.right:
                character.hitbox.right = self.true_hitbox.left
            elif character.hitbox.left <= self.true_hitbox.right <= character.hitbox.right:
                character.hitbox.left = self.true_hitbox.right
            character.on_wall = True
            # add frictional force for sliding on wall if the character is moving down
            if character.vel.y > 0 and character.name == 'ninja':
                character.y_forces.append(self.fric.y * character.vel.y)
            character.vel.x = 0
            character.rect.centerx = character.hitbox.centerx
        # handle vertical collisions with a wall
        elif axis == 'y':
            if (character.prev_hitbox.bottom - 1) <= self.true_hitbox.top <= character.hitbox.bottom: # falling
                character.hitbox.bottom = self.true_hitbox.top
                # wall applies normal force on character
                # make this force slightly less than gravity so there will still be some downward velocity
                character.y_forces.append(-GRAVITY*character.mass*0.99)
                # add frictional force for walking/running
                character.x_forces.append(self.fric.x * character.vel.x * character.mass)
                character.on_ground = True
            elif (character.prev_hitbox.top + 1) >= self.true_hitbox.bottom >= character.hitbox.top: # jumping
                character.hitbox.top = self.true_hitbox.bottom
            character.vel.y = 0
            character.rect.centery = character.hitbox.centery

    def update(self, dt):
        super().update(dt)
        for cue in self.dialog_cues:
            cue.hide()
        if self.hitbox.colliderect(self.scene.player.hitbox) and self.talking == False:
            self.dialog_cues[self.dialog_cue_index].show()
