import pygame.image

from ui.gui.maps.big_map.sprites.element import Element

image = pygame.image.load("assets/villager.png")

class UnitSprite(Element):
    def __init__(self, unit, isometry):
        self.unit = unit
        super().__init__(sprite_image=image, x=lambda: unit.get_position().get_x(), y=lambda: unit.get_position().get_y(), isometry=isometry)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        print("UnitSprite update")
        print(self.x(), self.y())
