from collections import deque

import pygame
from pygame.locals import *
from pygame_gui import UIManager
from pygame_gui.elements import UILabel

from tiled_levels.tiled_level import TiledLevel
from tiled_levels.map_editor import MapEditor
from collision.collision_grid import CollisionGrid
from game.gun_turret import GunTurret
from game.flame_turret import FlameTurret
from game.missile_turret import MissileTurret
from game.slow_turret import SlowTurret
from game.hud_button import HUDButton
from game.player_resources import PlayerResources
from game.splat import SplatLoader
from game.monster_wave_spawner import MonsterWaveSpawner
from game.main_menu import MainMenu
from game.select_level import SelectLevelMenu
from game.laser_turret import LaserTurret


class TurretCosts:
    def __init__(self):
        self.gun = 150
        self.flamer = 250
        self.missile = 400
        self.slow = 700
        self.laser = 500


class ScreenData:
    def __init__(self, hud_size, editor_hud_size, screen_size):
        self.screen_size = screen_size
        self.hud_dimensions = hud_size
        self.editor_hud_dimensions = editor_hud_size
        self.play_area = [screen_size[0], screen_size[1] - self.hud_dimensions[1]]

    def set_editor_active(self):
        self.play_area = [self.screen_size[0], self.screen_size[1] - self.editor_hud_dimensions[1]]


def display_normal_hud(hud_buttons, hud_sprites, turret_costs, screen_data, fonts, image_atlas):
    hud_buttons[:] = []
    hud_sprites.empty()
    hud_buttons.append(HUDButton([64, screen_data.screen_size[1] - 64], "gun_turret",
                                 turret_costs.gun, hud_sprites, fonts,
                                 image_atlas, [0, 384, 64, 64]))
    hud_buttons.append(HUDButton([160, screen_data.screen_size[1] - 64], "flame_turret",
                                 turret_costs.flamer, hud_sprites, fonts,
                                 image_atlas, [64, 384, 64, 64]))
    hud_buttons.append(HUDButton([256, screen_data.screen_size[1] - 64], "missile_turret",
                                 turret_costs.missile, hud_sprites, fonts,
                                 image_atlas, [128, 384, 64, 64]))
    hud_buttons.append(HUDButton([352, screen_data.screen_size[1] - 64], "slow_turret",
                                 turret_costs.slow, hud_sprites, fonts,
                                 image_atlas, [192, 384, 64, 64]))
    hud_buttons.append(HUDButton([448, screen_data.screen_size[1] - 64], "laser_turret",
                                 turret_costs.laser, hud_sprites, fonts,
                                 image_atlas, [256, 384, 64, 64]))


def display_upgrade_hud(hud_buttons, hud_sprites, turret, screen_data, fonts, image_atlas):
    hud_buttons[:] = []
    hud_sprites.empty()
    hud_buttons.append(HUDButton([64, screen_data.screen_size[1] - 64], "upgrade", turret.get_upgrade_cost(),
                                 hud_sprites, fonts, image_atlas, [384, 384, 64, 64]))
    hud_buttons.append(HUDButton([160, screen_data.screen_size[1] - 64], "sell", turret.get_sell_value(),
                                 hud_sprites, fonts, image_atlas, [448, 384, 64, 64]))


def main():
    pygame.init()
    pygame.key.set_repeat()
    x_screen_size = 1024
    y_screen_size = 600
    pygame.display.set_caption('Turret Warfare')
    screen = pygame.display.set_mode((x_screen_size, y_screen_size))

    background = pygame.Surface(screen.get_size())
    background = background.convert(screen)
    background.fill((95, 140, 95))

    ui_manager = UIManager(screen.get_size(), "data/ui_theme.json")
    fps_counter_label = None
    wave_display_label = None
    count_down_message_label = None

    static_sprite_surface = pygame.Surface(screen.get_size())
    should_redraw_static_sprites = True
    all_tile_sprites = pygame.sprite.Group()
    all_square_sprites = pygame.sprite.Group()
    all_monster_sprites = pygame.sprite.Group()
    all_turret_sprites = pygame.sprite.Group()
    all_bullet_sprites = pygame.sprite.Group()
    all_explosion_sprites = pygame.sprite.Group()
    splat_sprites = pygame.sprite.Group()
    hud_sprites = pygame.sprite.Group()
    explosions_sprite_sheet = pygame.image.load("images/explosions.png").convert_alpha()
    image_atlas = pygame.image.load("images/image_atlas.png").convert_alpha()
    splat_loader = SplatLoader()

    fonts = []
    font = pygame.font.Font(None, 32)
    large_font = pygame.font.Font(None, 64)
    title_font = pygame.font.Font("data/LondrinaShadow-Regular.ttf", 150)
    fun_small_font = pygame.font.Font("data/JustAnotherHand.ttf", 32)
    fun_large_font = pygame.font.Font("data/JustAnotherHand.ttf", 64)
    fun_very_small_font = pygame.font.Font("data/JustAnotherHand.ttf", 20)
    small_font = pygame.font.Font(None, 16)
    
    fonts.append(font)
    fonts.append(large_font)
    fonts.append(title_font)
    fonts.append(fun_small_font)
    fonts.append(fun_large_font)
    fonts.append(fun_very_small_font)
    fonts.append(small_font)

    mouse_active_turret = None

    explosions = []
    new_explosions = []
    bullets = []
    turrets = []
    monsters = []
    hud_buttons = []

    turret_costs = TurretCosts()

    screen_data = ScreenData([x_screen_size, 128], [x_screen_size, 184], [x_screen_size, y_screen_size])
    hud_rect = pygame.Rect(0, y_screen_size - 128, x_screen_size, 128)
    editor_hud_rect = pygame.Rect(0, screen_data.screen_size[1] - screen_data.editor_hud_dimensions[1],
                                  screen_data.editor_hud_dimensions[0], screen_data.editor_hud_dimensions[1])
    display_normal_hud(hud_buttons, hud_sprites, turret_costs, screen_data, fonts, image_atlas)

    main_menu = MainMenu(ui_manager)
    main_menu.start()
    select_level_menu = SelectLevelMenu(ui_manager)
    editor = None

    grid_size = 64
    screen_filling_number_of_grid_squares = [int(x_screen_size/grid_size),
                                             int(y_screen_size/grid_size)]
    collision_grid = CollisionGrid(screen_filling_number_of_grid_squares, grid_size)
    
    upgrade_hud_active = False
    active_upgrade_turret = None
    player_resources = PlayerResources()
    setup_time = 10.0
    setup_accumulator = 0.0
    is_setup = True
    should_show_count_down_message = False

    frame_rates = deque([])

    # load level data
    tiled_level = None
    monster_wave_spawner = None
    selected_level_path = ""
    clock = pygame.time.Clock()
    running = True
    is_main_menu = True
    is_map_editor = False
    is_select_level = False
    is_loading = False
    is_play_game = False
    is_game_over = False
    restart_game = False
    win_message = ""
    count_down_message = ""
    while running:
        frame_time = clock.tick(60)
        time_delta = min(frame_time/1000.0, 0.1)

        if is_main_menu:
            is_main_menu_and_index = main_menu.run(screen, time_delta)
            if is_main_menu_and_index[0] == 0:
                is_main_menu = True
            elif is_main_menu_and_index[0] == 1:
                is_main_menu = False
                is_select_level = True
                main_menu.end()
                select_level_menu.start()
            elif is_main_menu_and_index[0] == 2:
                running = False
        elif is_select_level:
            is_main_menu_and_index = select_level_menu.run(screen, time_delta)
            if is_main_menu_and_index[0] == 0:
                is_select_level = True
            elif is_main_menu_and_index[0] == 1:
                selected_level_path = select_level_menu.selected_level_path
                is_select_level = False
                is_loading = True
                select_level_menu.end()
            elif is_main_menu_and_index[0] == 2:
                selected_level_path = select_level_menu.selected_level_path
                tiled_level = TiledLevel(selected_level_path, [40, 21], all_tile_sprites, all_monster_sprites,
                                         all_square_sprites, image_atlas, monsters, screen_data,
                                         explosions_sprite_sheet)
                tiled_level.load_tiles()
                tiled_level.update_offset_position(tiled_level.find_player_start(), all_tile_sprites)
                
                editor = MapEditor(tiled_level, editor_hud_rect, fonts, all_square_sprites)
                is_map_editor = True
                is_select_level = False
                select_level_menu.end()
        elif is_loading:
            is_loading = False
            
            # clear level                
            tiled_level = TiledLevel(selected_level_path, [40, 21], all_tile_sprites, all_monster_sprites,
                                     all_square_sprites, image_atlas, monsters, screen_data, explosions_sprite_sheet)
            tiled_level.load_tiles()
            tiled_level.update_offset_position(tiled_level.find_player_start(), all_tile_sprites)
            monster_wave_spawner = MonsterWaveSpawner(monsters, tiled_level.monster_walk_path, 10, all_monster_sprites,
                                                      image_atlas, collision_grid, splat_loader)
           
            is_play_game = True
            restart_game = True
            should_redraw_static_sprites = True
            fps_counter_label = UILabel(pygame.Rect((900, 10), (100, 40)),
                                        "0 FPS", manager=ui_manager, object_id="#screen_text")

        elif is_map_editor:
            should_redraw_static_sprites = True
            screen_data.set_editor_active()
            running = editor.run(screen, background, all_tile_sprites, editor_hud_rect, time_delta)
        elif is_play_game:

            if not restart_game and is_setup:
                if setup_accumulator >= setup_time:
                    is_setup = False
                    setup_accumulator = 0.0
                elif setup_accumulator >= (setup_time - 6.0):
                    count_down_message = "First wave in " + str(int(setup_time - setup_accumulator)) + " seconds"
                    should_show_count_down_message = True
                    setup_accumulator += time_delta

                    if count_down_message_label is None:
                        count_down_message_label_rect = pygame.Rect((400, 10), (250, 40))
                        count_down_message_label_rect.centerx = screen_data.screen_size[0] / 2
                        count_down_message_label_rect.centery = 24
                        count_down_message_label = UILabel(count_down_message_label_rect,
                                                           count_down_message, manager=ui_manager,
                                                           object_id="#screen_text")
                else:
                    setup_accumulator += time_delta
                    remaining_time = str(int(setup_time - setup_accumulator))
                    count_down_message = "Setup Time remaining: " + remaining_time + " seconds"
                    should_show_count_down_message = True

                    if count_down_message_label is None:
                        count_down_message_label_rect = pygame.Rect((400, 10), (250, 40))
                        count_down_message_label_rect.centerx = screen_data.screen_size[0] / 2
                        count_down_message_label_rect.centery = 24
                        count_down_message_label = UILabel(count_down_message_label_rect,
                                                           count_down_message, manager=ui_manager,
                                                           object_id="#screen_text")
            elif restart_game:
                restart_game = False

                # clear all stuff
                explosions[:] = []
                new_explosions[:] = []
                bullets[:] = []
                turrets[:] = []
                monsters[:] = []
                hud_buttons[:] = []
                hud_sprites.empty()
                all_monster_sprites.empty()
                all_turret_sprites.empty()
                all_bullet_sprites.empty()
                all_explosion_sprites.empty()

                tiled_level.reset_squares()

                # reset player resources
                player_resources = PlayerResources()
                
                is_game_over = False
                is_setup = True
                setup_accumulator = 0.0
                monster_wave_spawner = MonsterWaveSpawner(monsters, tiled_level.monster_walk_path, 10,
                                                          all_monster_sprites, image_atlas, collision_grid,
                                                          splat_loader)
                mouse_active_turret = None
                active_upgrade_turret = None
                upgrade_hud_active = False
                should_show_count_down_message = False
                if count_down_message_label is not None:
                    count_down_message_label.kill()
                    count_down_message_label = None

                if wave_display_label is not None:
                    wave_display_label.kill()
                    wave_display_label = None

                display_normal_hud(hud_buttons, hud_sprites, turret_costs, screen_data, fonts, image_atlas)
                
            elif is_game_over:
                should_show_count_down_message = False
                if count_down_message_label is not None:
                    count_down_message_label.kill()
                    count_down_message_label = None
            else:
                monster_wave_spawner.update(time_delta, tiled_level.position_offset)
                if wave_display_label is not None:
                    wave_display_label.kill()
                    wave_display_label = None

                if monster_wave_spawner.should_show_wave_countdown:
                    should_show_count_down_message = True
                    count_down_message = monster_wave_spawner.count_down_message

                    if count_down_message_label is None:
                        count_down_message_label_rect = pygame.Rect((400, 10), (250, 40))
                        count_down_message_label_rect.centerx = screen_data.screen_size[0] / 2
                        count_down_message_label_rect.centery = 24
                        count_down_message_label = UILabel(count_down_message_label_rect,
                                                           count_down_message, manager=ui_manager,
                                                           object_id="#screen_text")
                else:
                    should_show_count_down_message = False
                    if count_down_message_label is not None:
                        count_down_message_label.kill()
                        count_down_message_label = None

                    if wave_display_label is None:
                        current_wave = str(monster_wave_spawner.current_wave_number)
                        max_wave = str(monster_wave_spawner.maximum_wave_number)
                        wave_display_label_rect = pygame.Rect((400, 10), (100, 40))
                        wave_display_label_rect.centerx = screen_data.screen_size[0] / 2
                        wave_display_label_rect.centery = 24
                        wave_display_label = UILabel(wave_display_label_rect,
                                                     "Wave " + current_wave + "/" + max_wave,
                                                     manager=ui_manager, object_id="#screen_text")

            if player_resources.current_base_health <= 0:
                is_game_over = True
                win_message = "You have been defeated!"

            on_final_wave = monster_wave_spawner.current_wave_number == monster_wave_spawner.maximum_wave_number
            if on_final_wave and len(monsters) == 0:
                is_game_over = True
                win_message = "You are victorious!"
                
            all_turret_sprites.empty()
            all_bullet_sprites.empty()
            all_explosion_sprites.empty()
                   
            # handle UI and inout events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                ui_manager.process_events(event)

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        is_main_menu = True
                        is_play_game = False
                        main_menu.start()
                        
                    if event.key == K_g:
                        monster_wave_spawner.wave_points = 1000
                        monster_wave_spawner.wave_time_accumulator = 5.0
                if is_game_over:
                    if event.type == KEYDOWN:
                        if event.key == K_y:
                            restart_game = True
                if not is_game_over and event.type == MOUSEBUTTONDOWN:
                    if event.button == 2:
                        if mouse_active_turret is not None:
                            turrets[:] = [turret for turret in turrets if turret is not mouse_active_turret]
                            mouse_active_turret = None
                    if event.button == 1:
                        clicked_on_any_hud_button = False
                        for hud_button in hud_buttons:
                            clicked_on_hud_button = hud_button.test_clicked(pygame.mouse.get_pos())
                            if clicked_on_hud_button:
                                clicked_on_any_hud_button = True
                            if clicked_on_hud_button:
                                if mouse_active_turret is not None:
                                    turrets[:] = [turret for turret in turrets if turret is not mouse_active_turret]
                                    mouse_active_turret = None
                                if upgrade_hud_active:
                                    if hud_button.button_name == "upgrade" and \
                                            player_resources.current_cash >= active_upgrade_turret.get_upgrade_cost():
                                        player_resources.current_cash -= active_upgrade_turret.get_upgrade_cost()
                                        active_upgrade_turret.upgrade()
                                        upgrade_hud_active = False
                                        active_upgrade_turret = None
                                        display_normal_hud(hud_buttons, hud_sprites, turret_costs,
                                                           screen_data, fonts, image_atlas)
                                    if hud_button.button_name == "sell":
                                        player_resources.current_cash += active_upgrade_turret.get_sell_value()
                                        for square in tiled_level.turret_squares:
                                            if square.rect.collidepoint(active_upgrade_turret.position):
                                                square.occupied = False
                                        turrets.remove(active_upgrade_turret)
                                        upgrade_hud_active = False
                                        active_upgrade_turret = None
                                        display_normal_hud(hud_buttons, hud_sprites, turret_costs,
                                                           screen_data, fonts, image_atlas)
                                else:
                                    new_turret = None
                                    if hud_button.button_name == "gun_turret":
                                        if turret_costs.gun <= player_resources.current_cash:
                                            new_turret = GunTurret(pygame.mouse.get_pos(), turret_costs.gun,
                                                                   explosions_sprite_sheet, image_atlas, collision_grid)
                                    if hud_button.button_name == "flame_turret":
                                        if turret_costs.flamer <= player_resources.current_cash:
                                            new_turret = FlameTurret(pygame.mouse.get_pos(), turret_costs.flamer,
                                                                     explosions_sprite_sheet, image_atlas,
                                                                     collision_grid)
                                    if hud_button.button_name == "missile_turret":
                                        if turret_costs.missile <= player_resources.current_cash:
                                            new_turret = MissileTurret(pygame.mouse.get_pos(), turret_costs.missile,
                                                                       explosions_sprite_sheet, image_atlas,
                                                                       collision_grid)
                                    if hud_button.button_name == "slow_turret":
                                        if turret_costs.slow <= player_resources.current_cash:
                                            new_turret = SlowTurret(pygame.mouse.get_pos(), turret_costs.slow,
                                                                    image_atlas)
                                    if hud_button.button_name == "laser_turret":
                                        if turret_costs.laser <= player_resources.current_cash:
                                            new_turret = LaserTurret(pygame.mouse.get_pos(), turret_costs.laser,
                                                                     image_atlas)
                                    if new_turret is not None:
                                        mouse_active_turret = new_turret
                                        turrets.append(new_turret)

                        if not clicked_on_any_hud_button:
                            if mouse_active_turret is not None:
                                is_in_placeable_location = False
                                for square in tiled_level.turret_squares:
                                    if square.rect.collidepoint(pygame.mouse.get_pos()) and not square.occupied:
                                        mouse_active_turret.set_position(square.position)
                                        is_in_placeable_location = True
                                        square.occupied = True
                                if is_in_placeable_location:
                                    player_resources.current_cash -= mouse_active_turret.build_cost
                                    mouse_active_turret.placed = True
                                    mouse_active_turret = None
                                    
                                else:
                                    turrets[:] = [turret for turret in turrets if turret is not mouse_active_turret]
                                    mouse_active_turret = None

                            else:
                                clicked_on_turret = False
                                for turret in turrets:
                                    if turret.rect.collidepoint(pygame.mouse.get_pos()):
                                        if turret.get_level() < turret.get_max_level():
                                            clicked_on_turret = True
                                            upgrade_hud_active = True
                                            display_upgrade_hud(hud_buttons, hud_sprites, turret,
                                                                screen_data, fonts, image_atlas)
                                            active_upgrade_turret = turret

                                if not clicked_on_turret and upgrade_hud_active:
                                    upgrade_hud_active = False
                                    display_normal_hud(hud_buttons, hud_sprites, turret_costs,
                                                       screen_data, fonts, image_atlas)

            if not is_game_over and mouse_active_turret is not None:
                is_over_square = False
                for square in tiled_level.turret_squares:
                    if square.rect.collidepoint(pygame.mouse.get_pos()) and not square.occupied:
                        mouse_active_turret.set_position(square.position)
                        mouse_active_turret.show_radius = True
                        is_over_square = True
                if not is_over_square:
                    mouse_active_turret.set_position(pygame.mouse.get_pos())
                    mouse_active_turret.show_radius = False

            for bullet in bullets:
                all_bullet_sprites = bullet.update_sprite(all_bullet_sprites)
                bullet.update_movement_and_collision(monsters, time_delta, new_explosions, explosions)
            bullets[:] = [bullet for bullet in bullets if not bullet.should_die]
            
            for monster in monsters:
                monster.update_movement_and_collision(time_delta, player_resources,
                                                      tiled_level.position_offset, splat_sprites)
                monster.update_sprite()
            monsters[:] = [monster for monster in monsters if not monster.should_die]
            new_explosions[:] = []
   
            for turret in turrets:
                turret.update_movement_and_collision(time_delta, monsters, bullets, pygame.mouse.get_pos())
                all_turret_sprites = turret.update_sprite(all_turret_sprites)
               
            for explosion in explosions:
                all_explosion_sprites = explosion.update_sprite(all_explosion_sprites, time_delta)
            explosions[:] = [explosion for explosion in explosions if not explosion.should_die]

            splat_sprites.update(time_delta)

            collision_grid.update_shape_grid_positions()
            collision_grid.check_collisions()

            ui_manager.update(time_delta)

            for collided_shape in collision_grid.shapes_collided_this_frame:
                if collided_shape.owner is not None:
                    collided_shape.owner.react_to_collision()

            if should_redraw_static_sprites:
                should_redraw_static_sprites = False
                static_sprite_surface.blit(background, (0, 0))  # draw the background
                all_tile_sprites.draw(static_sprite_surface)

            screen.blit(static_sprite_surface, (0, 0))
            splat_sprites.draw(screen)
            if mouse_active_turret is not None:
                all_square_sprites.draw(screen)
            all_monster_sprites.draw(screen)
            all_turret_sprites.draw(screen)
            all_bullet_sprites.draw(screen)
            all_explosion_sprites.draw(screen)

            # collision debug
            # for monster in monsters:
            #     monster.draw_collision_circle(screen)
            # for bullet in bullets:
            #     bullet.draw_collision_rect(screen)

            for turret in turrets:
                if turret.show_radius:
                    turret.draw_radius_circle(screen)
                
            pygame.draw.rect(screen, pygame.Color("#646464"), hud_rect, 0)  # draw the hud
            hud_sprites.draw(screen)
            for button in hud_buttons:
                button.draw_text(screen)

            cash_text_render = fonts[3].render("£" + "{:,}".format(player_resources.current_cash),
                                               True, pygame.Color("#FFFFFF"))
            cash_text_pos = [screen_data.hud_dimensions[0] * 0.9,
                             screen_data.screen_size[1] - (screen_data.hud_dimensions[1] * 0.8)]
            screen.blit(cash_text_render, cash_text_render.get_rect(centerx=cash_text_pos[0],
                                                                    centery=cash_text_pos[1]))

            health_text_render = fonts[3].render("Health: " + "{:,}".format(player_resources.current_base_health),
                                                 True, pygame.Color("#FFFFFF"))
            health_text_pos = [screen_data.hud_dimensions[0] * 0.9,
                               screen_data.screen_size[1] - (screen_data.hud_dimensions[1] * 0.5)]
            screen.blit(health_text_render, health_text_render.get_rect(centerx=health_text_pos[0],
                                                                        centery=health_text_pos[1]))

            if time_delta > 0.0 and fps_counter_label is not None:
                if len(frame_rates) < 300:
                    frame_rates.append(1.0/time_delta)
                else:
                    frame_rates.popleft()
                    frame_rates.append(1.0/time_delta)
                    
                fps = sum(frame_rates)/len(frame_rates)

                fps_counter_label.set_text("FPS: {:.2f}".format(fps))

            if should_show_count_down_message and count_down_message_label is not None:
                count_down_message_label.set_text(count_down_message)

            if wave_display_label is not None and monster_wave_spawner.has_changed_wave:
                current_wave = str(monster_wave_spawner.current_wave_number)
                max_wave = str(monster_wave_spawner.maximum_wave_number)
                wave_display_label.set_text("Wave " + current_wave + "/" + max_wave)

            if is_game_over:
                win_message_text_render = fonts[4].render(win_message, True, pygame.Color("#FFFFFF"))
                win_message_text_render_rect = win_message_text_render.get_rect(centerx=x_screen_size/2,
                                                                                centery=(y_screen_size/2)-128)
                play_again_text_render = fonts[3].render("Play Again? Press 'Y' to restart",
                                                         True, pygame.Color("#FFFFFF"))
                play_again_text_render_rect = play_again_text_render.get_rect(centerx=x_screen_size/2,
                                                                              centery=(y_screen_size/2)-90)
                screen.blit(win_message_text_render, win_message_text_render_rect)
                screen.blit(play_again_text_render, play_again_text_render_rect)

            ui_manager.draw_ui(screen)

        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()
