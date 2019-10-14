import pygame
from game.base_monster import BaseMonster


class StandardMonster(BaseMonster):
    monster_id = "standard"

    def __init__(self, monster_path, image_dictionary, monster_type_dict, all_monster_sprites, screen_offset,
                 collision_grid, splat_loader, ui_manager, *groups):
        image = image_dictionary[StandardMonster.monster_id]
        monster_type = monster_type_dict[StandardMonster.monster_id]
        super().__init__(monster_path, StandardMonster.monster_id, image, monster_type.points,
                         all_monster_sprites, screen_offset, collision_grid, splat_loader, ui_manager, *groups)
        self.setup_splat(pygame.Color("#79b176FF"))
        self.cash_value = 25
        self.move_speed = self.set_average_speed(70)
        self.set_starting_health(110)
