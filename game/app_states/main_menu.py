import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel

from .base_app_state import BaseAppState


class MainMenu(BaseAppState):

    def __init__(self, ui_manager: pygame_gui.UIManager, state_manger):
        super().__init__('main_menu', 'select_level', state_manger)

        self.ui_manager = ui_manager
        self.background_image = pygame.image.load("images/menu_background.png").convert()

        self.title_label = None
        self.play_game_button = None

    def start(self):
        self.title_label = UILabel(pygame.Rect((87, 40), (850, 180)), "Turret Warfare",
                                   self.ui_manager, object_id="#game_title")

        self.play_game_button = UIButton(pygame.Rect((437, 515), (150, 35)),
                                         "Start Game", self.ui_manager,
                                         tool_tip_text="<b>Click to Start.</b>")

    def end(self):
        self.title_label.kill()
        self.play_game_button.kill()

    def run(self, surface, time_delta):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.set_target_state_name('quit')
                self.trigger_transition()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_target_state_name('quit')
                    self.trigger_transition()
                
            self.ui_manager.process_events(event)
              
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.play_game_button:
                    self.set_target_state_name('select_level')
                    self.trigger_transition()

        self.ui_manager.update(time_delta)

        surface.blit(self.background_image, (0, 0))  # draw the background

        self.ui_manager.draw_ui(surface)
