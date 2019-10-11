import pygame


class HUDButton(pygame.sprite.Sprite):
    def __init__(self, start_pos, button_name, cost_data, hud_sprites, fonts, image_atlas, but_rec, *groups):
        super().__init__(*groups)
        self.clicked = False
        self.button_name = button_name
        self.image_atlas = image_atlas
        self.image_unclicked = self.image_atlas.subsurface((but_rec[0], but_rec[1], but_rec[2], but_rec[3]))
        self.image_clicked = self.image_atlas.subsurface((but_rec[0], but_rec[1] + 64, but_rec[2], but_rec[3]))

        self.image = self.image_unclicked
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        hud_sprites.add(self)

        # cost text
        self.font = fonts[5]
        cost_string = "£" + "{:,}".format(cost_data)
        self.cost_text_render = self.font.render(cost_string, True, pygame.Color("#FFFFFF"))
        self.text_pos = [start_pos[0], start_pos[1] + 48]

    def test_clicked(self, mouse_click_position):
        clicked = False
        if self.rect.collidepoint(mouse_click_position):
            self.image = self.image_clicked
            clicked = True
        if not clicked and self.clicked:
            self.clear_clicked()
        self.clicked = clicked
        return self.clicked

    def clear_clicked(self):
        self.clicked = False
        self.image = self.image_unclicked

    def draw_text(self, screen):
        screen.blit(self.cost_text_render, self.cost_text_render.get_rect(centerx=self.text_pos[0],
                                                                          centery=self.text_pos[1]))
