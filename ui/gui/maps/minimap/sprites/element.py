from math import radians, cos, sin

import pygame

from ui.gui.maps.big_map.sprites.entity import Entity
from ui.ui_manager import UIManager


class Element(Entity):
    def __init__(self, sprite_image, isometry, coef=1, x: callable = None, y: callable = None):
        """
        Sprite permettant de dessiner un élément sur la map

        :param sprite_image: Image du sprite
        :param isometry: Objet Isometry permettant de convertir les coordonnées réelle en isometrique
        :param coef: Coef multiplicateur de l'image
        :param x: Fonction retournant la position x du sprite (version normale, c'est à dire x au sens de la map et pas au sens isométrique)
        :param y: Fonction retournant la position y du sprite (version normale, c'est à dire y au sens de la map et pas au sens isométrique)
        """
        super().__init__(sprite_image, isometry, x, y)
        self.coef = coef

    def update_offset(self):
        iso_x, iso_y = self.isometry.x_y_to_iso(self.x(), self.y())
        game_width = UIManager.get_game().get_map().get_width()
        game_height = UIManager.get_game().get_map().get_height()
        offset_x = iso_x  + (pygame.display.get_surface().get_width()-1) - sin(radians(30)) * self.isometry.get_tile_length() * (game_width + game_height)
        offset_x = iso_x  + (pygame.display.get_surface().get_width()-1) - cos(radians(30)) * self.isometry.get_tile_length() * (game_width)

        offset_y = iso_y + (pygame.display.get_surface().get_height() - 1) - sin(radians(30)) * self.isometry.get_tile_length() * (game_width + game_height)
        #offset_x = iso_x #+ 100
        #offset_y = iso_y #+ 100
        self.rect.midbottom = (offset_x, offset_y)
        #print(self.rect.midbottom)

    def get_image_width(self):
        return cos(radians(30)) * self.isometry.get_tile_length() * (UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height())
        #return 2 * cos(radians(30)) * self.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()

    # def get_image_height(self):
    #     return 2 * sin(radians(30)) * self.isometry.get_tile_length() * UIManager.get_game().get_map().get_height()