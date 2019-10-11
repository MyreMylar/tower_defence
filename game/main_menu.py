import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel


class MainMenu:

    def __init__(self, ui_manager: pygame_gui.UIManager):

        self.ui_manager = ui_manager
        self.background_image = pygame.image.load("images/menu_background.png").convert()

        self.title_label = None
        self.play_game_button = None

    def start(self):
        self.title_label = UILabel(pygame.Rect((87, 40), (850, 178)), "Turret Warfare",
                                   self.ui_manager, object_id="#game_title")

        self.play_game_button = UIButton(pygame.Rect((437, 515), (150, 35)),
                                         "Start Game", self.ui_manager,
                                         tool_tip_text="<b>Click to Start.</b>")

    def end(self):
        self.title_label.kill()
        self.play_game_button.kill()

    def run(self, screen, time_delta):
        is_main_menu_and_index = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                is_main_menu_and_index[0] = 2
                
            self.ui_manager.process_events(event)
              
            if event.type == pygame.USEREVENT:
                if event.user_type == "ui_button_pressed":
                    if event.ui_element == self.play_game_button:
                        is_main_menu_and_index[0] = 1

        self.ui_manager.update(time_delta)

        screen.blit(self.background_image, (0, 0))  # draw the background

        self.ui_manager.draw_ui(screen)

        return is_main_menu_and_index
