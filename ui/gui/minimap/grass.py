import pygame
import math

from ui.gui.maps.big_map.sprites.entity import Entity
from ui.gui.maps.minimap.sprites.element import Element
from ui.gui.utils.isometry import Isometry
from ui.ui_manager import UIManager

# from ui.gui.maps.big_map.sprites import Element


class Grass(Element):
    def __init__(self, x, y, width, tile_length):
        #self.width = width
        super().__init__(pygame.image.load("grass.png"), Isometry(tile_length=lambda: tile_length), x=(lambda : x), y=lambda : y)
        self.update_offset()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        #print(self.rect.midbottom)

    def update_offset(self):
        self.rect.bottomright = (pygame.display.get_surface().get_width()-1, pygame.display.get_surface().get_height()-1)
