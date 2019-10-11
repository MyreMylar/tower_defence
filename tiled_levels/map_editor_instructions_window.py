import pygame
from game.ui_text_button import UTTextButton


class MapEditorInstructionsWindow:
    def __init__(self, window_rect, fonts):
        self.window_rect = window_rect
        self.fonts = fonts
        self.background_colour = pygame.Color("#151515")
        self.text_colour = pygame.Color("#FFFFFF")
        
        self.window_title_str = "Instructions"
        self.title_text_render = self.fonts[1].render(self.window_title_str, True, self.text_colour)

        self.should_exit = False

        self.done_button = UTTextButton([self.window_rect[0] + (self.window_rect[2] / 2) + 45,
                                         self.window_rect[1] + self.window_rect[3] - 30, 70, 20], "Done", fonts, 0)

        self.instructions_text_1 = "Arrow keys to scroll map"
        self.instructions_text_2 = "Left mouse click to select tile from palette"
        self.instructions_text_3 = "Right mouse click to place tile"
        self.instructions_text_4 = "'>' and '<' to rotate selected tile"
        self.instructions_text_5 = "F5 or quit to save map"

        self.window_x_centre = self.window_rect[0] + self.window_rect[2] * 0.5

        self.instructions_text_render_1 = self.fonts[6].render(self.instructions_text_1, True, self.text_colour)
        self.instructions_text_render_2 = self.fonts[6].render(self.instructions_text_2, True, self.text_colour)
        self.instructions_text_render_3 = self.fonts[6].render(self.instructions_text_3, True, self.text_colour)
        self.instructions_text_render_4 = self.fonts[6].render(self.instructions_text_4, True, self.text_colour)
        self.instructions_text_render_5 = self.fonts[6].render(self.instructions_text_5, True, self.text_colour)

    def handle_input_event(self, event):
        self.done_button.handle_input_event(event)

    def update(self):
        self.done_button.update()

        if self.done_button.was_pressed():
            self.should_exit = True

    def is_inside(self, screen_pos):
        is_inside = False
        if self.window_rect[0] <= screen_pos[0] <= self.window_rect[0] + self.window_rect[2]:
            if self.window_rect[1] <= screen_pos[1] <= self.window_rect[1] + self.window_rect[3]:
                is_inside = True
        return is_inside

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_colour, pygame.Rect(self.window_rect[0], self.window_rect[1],
                                                                     self.window_rect[2], self.window_rect[3]), 0)

        screen.blit(self.title_text_render,
                    self.title_text_render.get_rect(centerx=self.window_rect[0] + self.window_rect[2] * 0.5,
                                                    centery=self.window_rect[1] + 24))

        screen.blit(self.instructions_text_render_1,
                    self.instructions_text_render_1.get_rect(centerx=self.window_x_centre,
                                                             centery=self.window_rect[1] + 50))
        screen.blit(self.instructions_text_render_2,
                    self.instructions_text_render_2.get_rect(centerx=self.window_x_centre,
                                                             centery=self.window_rect[1] + 64))
        screen.blit(self.instructions_text_render_3,
                    self.instructions_text_render_3.get_rect(centerx=self.window_x_centre,
                                                             centery=self.window_rect[1] + 78))
        screen.blit(self.instructions_text_render_4,
                    self.instructions_text_render_4.get_rect(centerx=self.window_x_centre,
                                                             centery=self.window_rect[1] + 92))
        screen.blit(self.instructions_text_render_5,
                    self.instructions_text_render_5.get_rect(centerx=self.window_x_centre,
                                                             centery=self.window_rect[1] + 106))
        
        self.done_button.draw(screen)
