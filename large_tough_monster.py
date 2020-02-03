import pygame
from game.base_monster import BaseMonster


# ------------------------------------------------------------------------
# Challenge 2 - part A
# ---------------------
#
# We are going to add the large, tough monster to the enemy list.
#
# 1. The first thing to do is increase this guy's starting health to about
#    1500.
# 2. Next reduce the monster's average speed a little (to 40); all that muscle
#    slows these fellows down.
# 3. Increase the cash you get for killing one to 200
#
# -------------------------------------------------------------------
# Challenge 2 is continued in the 'monster_wave_spawner' code file.
# -------------------------------------------------------------------
class LargeToughMonster(BaseMonster):
    monster_id = "large_tough"

    def __init__(self, monster_path, image_dictionary, monster_type_dict,
                 all_monster_sprites, screen_offset, collision_grid, splat_loader, ui_manager, *groups):
        image = image_dictionary[LargeToughMonster.monster_id]
        monster_type = monster_type_dict[LargeToughMonster.monster_id]
        super().__init__(monster_path, LargeToughMonster.monster_id, image, monster_type.points,
                         all_monster_sprites, screen_offset,
                         collision_grid, splat_loader, ui_manager, *groups)
        self.setup_splat(pygame.Color("#20afc9FF"))
        self.cash_value = 100
        self.move_speed = self.set_average_speed(60)
        self.set_starting_health(100)
