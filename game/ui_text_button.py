import pygame
from pygame.locals import *


class UTTextButton:
    def __init__(self, rect, button_text, fonts, font_size,
                 button_col=pygame.Color("#4B4B4B"), text_col=pygame.Color("#FFFFFF")):
        self.fonts = fonts
        self.button_text = button_text
        self.rect = rect
        self.started_button_click = False
        self.clicked_button = False
        self.is_hovered = True
        self.font_size = font_size

        self.is_enabled = True
        self.is_selected = False

        self.button_colour = button_col
        self.text_colour = text_col

        self.normal_button_colour = button_col
        self.normal_text_colour = text_col
        self.hovered_button_col = pygame.Color("#000000")
        self.hovered_button_col.r = min(255, self.button_colour.r + 25)
        self.hovered_button_col.g = min(255, self.button_colour.g + 25)
        self.hovered_button_col.b = min(255, self.button_colour.b + 25)

        self.selected_button_col = pygame.Color("#000000")
        self.selected_button_col.r = min(255, self.button_colour.r + 40)
        self.selected_button_col.g = min(255, self.button_colour.g + 40)
        self.selected_button_col.b = min(255, self.button_colour.b + 40)
        
        self.disabled_button_col = pygame.Color("#000000")
        self.disabled_button_col.r = max(0, self.button_colour.r - 25)
        self.disabled_button_col.g = max(0, self.button_colour.g - 25)
        self.disabled_button_col.b = max(0, self.button_colour.b - 25)
        self.disabled_text_col = pygame.Color("#000000")

        self.button_text_render = self.fonts[self.font_size].render(self.button_text, True, self.text_colour)

    def handle_input_event(self, event):
        if self.is_enabled and self.is_inside(pygame.mouse.get_pos()):
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.started_button_click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and self.started_button_click:
                    self.clicked_button = True
                    self.started_button_click = False
                    
    def disable(self):
        self.is_enabled = False
        self.button_colour = self.disabled_button_col
        self.text_colour = self.disabled_text_col

    def enable(self):
        self.is_enabled = True
        self.button_colour = self.normal_button_colour
        self.text_colour = self.normal_text_colour

    def set_selected(self):
        self.is_selected = True
        self.button_colour = self.selected_button_col
        self.text_colour = self.normal_text_colour

    def set_unselected(self):
        self.is_selected = False
        self.button_colour = self.normal_button_colour
        self.text_colour = self.normal_text_colour
        
    def set_hovered(self):
        self.is_hovered = True
        self.button_colour = self.hovered_button_col

    def set_unhovered(self):
        self.is_hovered = False
        if self.is_selected:
            self.button_colour = self.selected_button_col
        else:
            self.button_colour = self.normal_button_colour
    
    def was_pressed(self):
        was_pressed = self.clicked_button
        self.clicked_button = False
        return was_pressed

    def set_text(self, text):
        self.button_text = text
        self.button_text_render = self.fonts[self.font_size].render(self.button_text, True, self.text_colour)
    
    def update(self):
        if self.is_enabled and self.is_inside(pygame.mouse.get_pos()):
            self.set_hovered()
        elif self.is_enabled:
            self.set_unhovered()

    def is_inside(self, screen_pos):
        is_inside = False
        if self.rect[0] <= screen_pos[0] <= self.rect[0]+self.rect[2]:
            if self.rect[1] <= screen_pos[1] <= self.rect[1]+self.rect[3]:
                is_inside = True
        return is_inside

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_colour,
                         pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 0)
        screen.blit(self.button_text_render,
                    self.button_text_render.get_rect(centerx=self.rect[0] + self.rect[2] * 0.5,
                                                     centery=self.rect[1] + self.rect[3] * 0.5))
