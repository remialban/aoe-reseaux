import pygame
from math import cos, radians, sin
from ui.gui.maps.minimap.sprites.element import Element
from ui.ui_manager import UIManager

#image = pygame.image.load("assets/minimap/building.png")
images = {
    "MAGENTA": pygame.image.load("assets/minimap/MAGENTA.png"),
    "RED": pygame.image.load("assets/minimap/RED.png"),
    "BLUE": pygame.image.load("assets/minimap/BLUE.png"),
    "GREEN": pygame.image.load("assets/minimap/GREEN.png"),
    "YELLOW": pygame.image.load("assets/minimap/YELLOW.png"),
    "CYAN": pygame.image.load("assets/minimap/CYAN.png"),
    "WHITE": pygame.image.load("assets/minimap/WHITE.png")
}
class BuildingSprite(Element):
    def __init__(self, building, isometry):
        self.resource = building
        self.building = building
        super().__init__(images.get(building.get_player().get_color()), isometry, x=lambda: building.get_position().get_x() + building.get_width(), y=lambda: building.get_position().get_y() + building.get_height())
        self.update_offset()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.update_offset()

    def get_image_width(self):
        return 2* cos(radians(30)) * self.isometry.get_tile_length() * self.building.get_width()

        return self.building.get_width() * self.building.get_width()


