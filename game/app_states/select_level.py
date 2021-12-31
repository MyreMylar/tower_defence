import os

import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel


from .base_app_state import BaseAppState


class LevelUIData:
    def __init__(self, level_path):
        self.path = level_path
        self.display_name = level_path.split('/')[-1].split('.')[0].replace('_', ' ').capitalize()


class SelectLevelMenu(BaseAppState):
    def __init__(self, ui_manager: pygame_gui.UIManager, state_manager):
        super().__init__('select_level', 'game', state_manager)
        self.ui_manager = ui_manager
        self.all_level_paths = []
        self.selected_level_path = None
        self.background_image = None
        self.title_label = None
        self.play_game_button = None
        self.edit_map_button = None
        self.level_button_group = []
        self.level_group_y_start = 100
        self.reload_levels()

    def start(self):
        self.level_group_y_start = 100
        self.selected_level_path = self.all_level_paths[0].path
   
        self.background_image = pygame.image.load("images/menu_background.png").convert()

        self.title_label = UILabel(pygame.Rect((400, 25), (230, 62)), "Select Level",
                                   self.ui_manager, object_id="#game_sub_title")

        self.play_game_button = UIButton(pygame.Rect((437, 515), (150, 35)),
                                         "Start Level", self.ui_manager,
                                         tool_tip_text="<b>Click to start level.</b>")

        self.edit_map_button = UIButton(pygame.Rect((437, 555), (150, 35)),
                                        "Edit Level", self.ui_manager,
                                        tool_tip_text="<b>Click to enter the level editor.</b>")

        for level_data in self.all_level_paths:
            self.level_button_group.append(UIButton(pygame.Rect((437, self.level_group_y_start),
                                                                (150, 20)),
                                                    level_data.display_name,
                                                    self.ui_manager,
                                                    tool_tip_text="<b>Select this level.</b>",
                                                    object_id="#choose_level_button"))
            self.level_group_y_start += 25
            
        if len(self.level_button_group) > 0:
            self.ui_manager.set_focus_set(self.level_button_group[0])

    def end(self):
        self.title_label.kill()
        self.play_game_button.kill()
        self.edit_map_button.kill()
        for button in self.level_button_group:
            button.kill()
        self.level_button_group.clear()

    def reload_levels(self):
        self.all_level_paths[:] = []
        for level_file in os.listdir("data/levels/"):
            full_file_name = "data/levels/" + level_file
            level_data = LevelUIData(full_file_name)
            self.all_level_paths.append(level_data)
              
    def run(self, surface, time_delta):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.set_target_state_name('quit')
                self.trigger_transition()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.trigger_transition()

            self.ui_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.play_game_button:
                    self.set_target_state_name('game')
                    self.outgoing_transition_data['selected_level_path'] = self.selected_level_path
                    self.trigger_transition()

                if event.ui_element == self.edit_map_button:
                    self.set_target_state_name('editor')
                    self.outgoing_transition_data['selected_level_path'] = self.selected_level_path
                    self.trigger_transition()

                if event.ui_object_id == "#choose_level_button":
                    self.ui_manager.set_focus_set(event.ui_element)
                    for level_data in self.all_level_paths:
                        if level_data.display_name == event.ui_element.text:
                            self.selected_level_path = level_data.path

        self.ui_manager.update(time_delta)

        surface.blit(self.background_image, (0, 0))  # draw the background
        self.ui_manager.draw_ui(surface)
