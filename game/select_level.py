import pygame
import os
from pygame.locals import *
from game.ui_text_button import UTTextButton


class LevelUIData:
    def __init__(self, level_path):
        self.path = level_path
        self.display_name = level_path.split('/')[-1].split('.')[0].replace('_', ' ').capitalize()


class SelectLevelMenu:
    def __init__(self, fonts, screen_data):
        self.all_level_paths = []
        self.reload_levels()
        self.selected_level_path = self.all_level_paths[0].path
   
        self.background_image = pygame.image.load("images/menu_background.png").convert()

        self.menu_title_text_render = fonts[0].render("Select Level", True, pygame.Color("#000000"))
        self.menu_title_text_rect = self.menu_title_text_render.get_rect(centerx=screen_data.screen_size[0] * 0.5,
                                                                         centery=50)

        self.play_game_button = UTTextButton([437, 515, 150, 35], "Start Level", fonts, 0,
                                             pygame.Color("#646473"), pygame.Color("#FFFFFF"))

        self.edit_map_button = UTTextButton([437, 555, 150, 35], "Edit Level", fonts, 0,
                                            pygame.Color("#646473"), pygame.Color("#FFFFFF"))

        self.level_button_group = []
        self.level_group_y_start = 100
        for level_data in self.all_level_paths:
            self.level_button_group.append(UTTextButton([437, self.level_group_y_start, 150, 20],
                                                        level_data.display_name,
                                                        fonts, 0, pygame.Color("#32323C"), pygame.Color("#FFFFFF")))
            self.level_group_y_start += 25
            
        if len(self.level_button_group) > 0:
            self.level_button_group[0].set_selected()

    def reload_levels(self):
        self.all_level_paths[:] = []
        for level_file in os.listdir("data/levels/"):
            full_file_name = "data/levels/" + level_file
            level_data = LevelUIData(full_file_name)
            self.all_level_paths.append(level_data)
              
    def run(self, screen):
        is_main_menu_and_index = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                is_main_menu_and_index[0] = 2
                
            self.play_game_button.handle_input_event(event)
            self.edit_map_button.handle_input_event(event)

            for button in self.level_button_group:
                button.handle_input_event(event)
              
            if event.type == QUIT:
                is_main_menu_and_index[0] = 2

        self.play_game_button.update()
        self.edit_map_button.update()

        screen.blit(self.background_image, (0, 0))  # draw the background

        for button in self.level_button_group:
            button.update()
            if button.was_pressed():
                for clear_button in self.level_button_group:
                    clear_button.set_unselected()
                button.set_selected()
                for level_data in self.all_level_paths:
                    if level_data.display_name == button.button_text:
                        self.selected_level_path = level_data.path
            button.draw(screen)
                
        if self.play_game_button.was_pressed():
            is_main_menu_and_index[0] = 1
        if self.edit_map_button.was_pressed():
            is_main_menu_and_index[0] = 2

        screen.blit(self.menu_title_text_render, self.menu_title_text_rect)

        self.play_game_button.draw(screen)
        self.edit_map_button.draw(screen)

        return is_main_menu_and_index
