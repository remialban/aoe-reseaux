import pygame
import math

from ui.gui.utils.camera import Camera
from ui.gui.utils.isometry import Isometry
from .element import Element

grass_image10 = pygame.image.load("assets/grass10.png")
grass_image = pygame.image.load("assets/grass.png")

class Grass(Element):
    def __init__(self, x, y, width=1, height=0):
        self.width = width
        super().__init__(grass_image if width == 1 else grass_image10, Isometry(tile_length=Camera.get_tile_length), x=(lambda : x), y=lambda : y)
        self.update_offset()

    def get_image_height(self):
        return self.isometry.get_tile_length() * 2 * math.cos(math.radians(60)) * self.width

    def get_image_width(self):
        return super().get_image_width() * self.width