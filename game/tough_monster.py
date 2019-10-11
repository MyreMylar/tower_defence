import pygame
from game.base_monster import BaseMonster


class ToughMonster(BaseMonster):
    monster_id = "tough"

    def __init__(self, monster_path, image_dictionary, monster_type_dict,
                 all_monster_sprites, screen_offset, collision_grid, splat_loader, *groups):
        image = image_dictionary[ToughMonster.monster_id]
        monster_type = monster_type_dict[ToughMonster.monster_id]
        super().__init__(monster_path, ToughMonster.monster_id, image, monster_type.points,
                         all_monster_sprites, screen_offset, collision_grid, splat_loader, *groups)
        self.setup_splat(pygame.Color("#20afc9FF"))
        self.cash_value = 45
        self.move_speed = self.set_average_speed(60)
        self.health = 170
