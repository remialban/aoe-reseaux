import pygame.sprite

from ui.gui.utils.camera import Camera

import math

from ui.gui.const import TILE_WIDTH


class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite_image, isometry, x: callable = None, y: callable = None):
        """
        Sprite permettant de dessiner un élément sur la maps

        :param sprite_image: Image du sprite
        :param isometry: Objet Isometry permettant de convertir les coordonnées réelle en isometrique
        :param coef: Coef multiplicateur de l'image
        :param x: Fonction retournant la position x du sprite (version normale, c'est à dire x au sens de la maps et pas au sens isométrique)
        :param y: Fonction retournant la position y du sprite (version normale, c'est à dire y au sens de la maps et pas au sens isométrique)
        """
        super().__init__()
        self.isometry = isometry
        self.tile_length = isometry.get_tile_length()
        self.sprite_image = sprite_image

        self.generate_image()

        self.x = x
        self.y = y
        self.previous_x = x()
        self.previous_y = y()


    def update_offset(self):
        iso_x, iso_y = self.isometry.x_y_to_iso(self.x(), self.y())
        new_x, new_y = Camera.apply_offset(iso_x, iso_y)
        self.rect.midbottom = (new_x, new_y)


    # def apply_coordinate(self):
    #     if self.previous_x != self.x() or self.previous_y != self.y():
    #         self.previous_x = self.x()
    #         self.previous_y = self.y()
    #         self.rect.midbottom = (self.x(), self.y())

    def generate_image(self):
        width = self.get_image_width()
        height = self.get_image_height()
        self.image = pygame.transform.scale(self.sprite_image, (width, height))
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs):
        if self.tile_length != self.isometry.get_tile_length():
            self.tile_length = self.isometry.get_tile_length()
            self.generate_image()

        self.update_offset()
        super().update(*args, **kwargs)

    def get_image_width(self):
        return 2 * math.sin(math.radians(60)) * self.isometry.get_tile_length()

    def get_image_height(self):
        return self.get_image_width() * self.sprite_image.get_height() / self.sprite_image.get_width()