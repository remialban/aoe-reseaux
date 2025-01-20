import pygame
from math import cos, radians, sin

from core.resources_points.mine import Mine
from core.resources_points.wood import Wood
from ui.gui.maps.minimap.sprites.element import Element
from ui.ui_manager import UIManager

#image = pygame.image.load("assets/minimap/building.png")
images = {
    "WOOD": pygame.image.load("assets/minimap/WOOD.png"),
    "GOLD": pygame.image.load("assets/minimap/GOLD.png")
}
class ResourcePointSprite(Element):
    def __init__(self, resource, isometry):
        self.resource = resource
        image = None
        match resource:
            case Wood():
                image = images.get("WOOD")
            case Mine():
                image = images.get("GOLD")
        super().__init__(image, isometry, x=lambda: resource.get_position().get_x() + 1, y=lambda: resource.get_position().get_y() + 1)
        self.update_offset()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.update_offset()

    def get_image_width(self):
        return max(2* cos(radians(30)) * self.isometry.get_tile_length(), 4)


