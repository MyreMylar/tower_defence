#!/usr/bin/env python3

import os

import pygame
from pygame_gui import UIManager

from game.app_states.app_state_manager import AppStateManager
from game.app_states.main_menu import MainMenu
from game.app_states.select_level import SelectLevelMenu
from game.app_states.quit_state import QuitState
from game.app_states.game_state import GameState
from game.app_states.editor_state import EditorState


class ScreenData:
    def __init__(self, hud_size, editor_hud_size, screen_size):
        self.screen_size = screen_size
        self.hud_dimensions = hud_size
        self.editor_hud_dimensions = editor_hud_size
        self.play_area = [screen_size[0], screen_size[1] - self.hud_dimensions[1]]

    def set_editor_active(self):
        self.play_area = [self.screen_size[0], self.screen_size[1] - self.editor_hud_dimensions[1]]

    def set_editor_inactive(self):
        self.play_area = [self.screen_size[0], self.screen_size[1] - self.hud_dimensions[1]]


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.key.set_repeat()
    x_screen_size = 1024
    y_screen_size = 600
    pygame.display.set_caption('Turret Warfare')
    screen = pygame.display.set_mode((x_screen_size, y_screen_size))

    screen_data = ScreenData([x_screen_size, 128], [x_screen_size, 184], [x_screen_size, y_screen_size])

    ui_manager = UIManager(screen.get_size(), "data/ui_theme.json")
    ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                              {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                              {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])

    app_state_manager = AppStateManager()
    MainMenu(ui_manager, app_state_manager)
    SelectLevelMenu(ui_manager, app_state_manager)
    GameState(ui_manager, screen, screen_data, app_state_manager)
    EditorState(ui_manager, screen, screen_data, app_state_manager)
    QuitState(app_state_manager)
    app_state_manager.set_initial_state('main_menu')

    clock = pygame.time.Clock()
    running = True

    while running:
        frame_time = clock.tick(60)
        time_delta = min(frame_time/1000.0, 0.1)

        running = app_state_manager.run(screen, time_delta)

        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()
