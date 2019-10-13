import pygame
import pygame_gui
from pygame_gui.elements import UILabel

from .base_app_state import BaseAppState
from tiled_levels.tiled_level import TiledLevel
from tiled_levels.map_editor import MapEditor


class EditorState(BaseAppState):

    def __init__(self, ui_manager: pygame_gui.UIManager, screen_surface, screen_data, state_manager):
        super().__init__('editor', 'main_menu', state_manager)

        self.ui_manager = ui_manager
        self.screen_surface = screen_surface
        self.screen_data = screen_data

        self.level_to_load_path = None

        self.background = None

        self.fonts = []
        self.monsters = []

        # objects
        self.tiled_level = None
        self.editor = None

        # sprite groups
        self.all_tile_sprites = None
        self.all_square_sprites = None
        self.all_monster_sprites = None

        # images
        self.explosions_sprite_sheet = None
        self.image_atlas = None

        self.should_redraw_static_sprites = False

        self.editor_hud_rect = None

    def start(self):
        # hud_rect = pygame.Rect(0, y_screen_size - 128, x_screen_size, 128)
        self.editor_hud_rect = pygame.Rect(0,
                                           self.screen_data.screen_size[1] - self.screen_data.editor_hud_dimensions[1],
                                           self.screen_data.editor_hud_dimensions[0],
                                           self.screen_data.editor_hud_dimensions[1])

        font = pygame.font.Font(None, 32)
        large_font = pygame.font.Font(None, 64)
        title_font = pygame.font.Font("data/LondrinaShadow-Regular.ttf", 150)
        fun_small_font = pygame.font.Font("data/JustAnotherHand.ttf", 32)
        fun_large_font = pygame.font.Font("data/JustAnotherHand.ttf", 64)
        fun_very_small_font = pygame.font.Font("data/JustAnotherHand.ttf", 20)
        small_font = pygame.font.Font(None, 16)

        self.fonts.append(font)
        self.fonts.append(large_font)
        self.fonts.append(title_font)
        self.fonts.append(fun_small_font)
        self.fonts.append(fun_large_font)
        self.fonts.append(fun_very_small_font)
        self.fonts.append(small_font)

        self.background = pygame.Surface(self.screen_surface.get_size())
        self.background = self.background.convert(self.screen_surface)
        self.background.fill((95, 140, 95))

        self.all_tile_sprites = pygame.sprite.Group()
        self.all_square_sprites = pygame.sprite.Group()
        self.all_monster_sprites = pygame.sprite.Group()

        self.explosions_sprite_sheet = pygame.image.load("images/explosions.png").convert_alpha()
        self.image_atlas = pygame.image.load("images/image_atlas.png").convert_alpha()

        self.level_to_load_path = self.incoming_transition_data['selected_level_path']
        self.tiled_level = TiledLevel(self.level_to_load_path, [40, 21], self.all_tile_sprites,
                                      self.all_monster_sprites, self.all_square_sprites,
                                      self.image_atlas, self.monsters, self.screen_data,
                                      self.explosions_sprite_sheet)
        self.tiled_level.load_tiles()
        self.tiled_level.update_offset_position(self.tiled_level.find_player_start(), self.all_tile_sprites)

        self.editor = MapEditor(self.tiled_level, self.editor_hud_rect, self.fonts, self.all_square_sprites)

    def end(self):
        pass

    def run(self, surface, time_delta):
        self.should_redraw_static_sprites = True
        self.screen_data.set_editor_active()
        self.editor.run(surface, self.background, self.all_tile_sprites,
                        self.editor_hud_rect, time_delta)
