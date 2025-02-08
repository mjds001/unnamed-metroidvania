import pygame

from settings import *

"""
Dialog box class to handle displaying text at the top of the screen.

Dialog for dialog boxes is written in the "dialog" custom property of the npc object within
the level editor. Different slides of dialog are separated by /n characters.
"""


class DialogBox(pygame.sprite.Sprite):
    def __init__(self, game, text, groups, choices=None, z='ui'):
        super().__init__(groups)
        self.text = text
        self.text_color = COLORS['white']
        self.game = game
        self.font = pygame.font.Font(FONT, 12)
        self.visible = False
        self.box_rect = pygame.Rect(20, 20, SCREEN_WIDTH - 40, 100)
        self.text_rect = self.box_rect.inflate(-40, -40)
        self.type_speed = 100 # characters per second
        self.text_index = 0
        self.lines = self.break_text_into_lines()
        self.line_index = 0
        self.full_dialog_shown = False

        # optional choices for player input
        self.choices = choices if choices else []
        self.selected_index = 0

    def break_text_into_lines(self):
        # if the text is longer than the text box, break it up into multiple lines
        # and store the lines in a list
        words = self.text.split(' ')
        lines = []
        line = ''
        for word in words:
            test_line = f'{line} {word}'.strip()
            if self.font.size(test_line)[0] <= self.text_rect.width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)

        return lines
    
    def show_full_dialog(self):
        self.line_index = len(self.lines)
        self.text_index = len(self.lines[self.line_index - 1])

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
        self.text_index = 0
        self.line_index = 0
        self.selected_index = 0
        self.full_dialog_shown = False

    def render_text(self, text, screen, pos, color = COLORS['white']):
        surf = self.font.render(str(text), False, color=color)
        rect = surf.get_rect(topleft = pos)
        screen.blit(surf, rect)

    def handle_input(self):
        if self.visible and self.choices:
            if INPUTS['left']:
                self.selected_index = min(max(self.selected_index - 1, 0), len(self.choices) - 1)
                self.game.reset_inputs()
            if INPUTS['right']:
                self.selected_index = min(max(self.selected_index + 1, 0), len(self.choices) - 1)
                self.game.reset_inputs()

    def update(self, dt):
        if self.visible:
            if self.choices:
                self.handle_input()
            # if the line index is greater than the number of lines, stop updating
            if self.line_index >= len(self.lines):
                self.full_dialog_shown = True
                return
            # increase the text index based on the type speed
            self.text_index += self.type_speed * dt
            # if the text index is greater than the length of the current line, increase the line index
            if self.text_index > len(self.lines[self.line_index]):
                self.line_index += 1
                self.text_index = 0

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, COLORS['black'], self.box_rect, border_radius=15)
            pygame.draw.rect(screen, COLORS['white'], self.box_rect, 2, border_radius=15)
            # draw the text
            for i, line in enumerate(self.lines):
                if i < self.line_index:
                    self.render_text(line, screen, (self.text_rect.x, self.text_rect.y + i * 15))
                elif i == self.line_index:
                    self.render_text(line[:int(self.text_index)], screen, (self.text_rect.x, self.text_rect.y + i * 15))
                else:
                    break
            
            # draw the choices
            if self.choices and self.full_dialog_shown:
                for i, choice in enumerate(self.choices):
                    color = self.text_color
                    # offset x position by width of each previous choice
                    previous_choices_width = sum([self.font.size(self.choices[j])[0] for j in range(i)]) + 20 * i
                    pos = (self.text_rect.x + previous_choices_width, self.text_rect.y + (len(self.lines) + 1) * 15)
                    if i == self.selected_index:
                        color = COLORS['yellow']
                        self.render_text('>', screen, (pos[0]-10, pos[1]), color)
                    self.render_text(choice, screen, pos, color)