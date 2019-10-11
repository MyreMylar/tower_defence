import pygame
from pygame.locals import *

from game.ui_text_button import UTTextButton

# ------------------------------------------------------
# Challenge 1 - Using # comments to 'comment out' code 
# ------------------------------------------------------
#
# Figure out how to enable the 'play game' button!
#
# TIP
# -----
# - You will need to comment out one line of code
#   that is currently disabling the button.
#
# -----------------------
# Challenge 2 starts in the 'large_tough_monster' file
# ------------------------------------------------------


class MainMenu:

    def __init__(self, fonts, screen_data):
   
        self.backgroundImage = pygame.image.load("images/menu_background.png").convert()

        main_menu_title_string = "Turret Warfare"
        self.title_text_render = fonts[2].render(main_menu_title_string, True, pygame.Color("#000000"))
        self.title_text_render_rect = self.title_text_render.get_rect(centerx=screen_data.screen_size[0] * 0.5,
                                                                      centery=80)

        self.play_game_button = UTTextButton([437, 515, 150, 35], "Start Game", fonts, 0,
                                             pygame.Color("#646473"), pygame.Color("#FFFFFF"))
      
        # self.play_game_button.disable()
        
    def run(self, screen):
        is_main_menu_and_index = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                is_main_menu_and_index[0] = 2
                
            self.play_game_button.handle_input_event(event)
              
            if event.type == QUIT:
                is_main_menu_and_index[0] = 2

        self.play_game_button.update()

        if self.play_game_button.was_pressed():
            is_main_menu_and_index[0] = 1
                    
        screen.blit(self.backgroundImage, (0, 0))  # draw the background
        screen.blit(self.title_text_render, self.title_text_render_rect)

        self.play_game_button.draw(screen)

        return is_main_menu_and_index
