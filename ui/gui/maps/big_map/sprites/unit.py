import pygame.image

from core.units.archer import Archer
from core.units.horse_man import Horseman
from core.units.swordsman import Swordsman
from core.units.villager import Villager
from ui.gui.maps.big_map.sprites.element import Element

image = pygame.image.load("assets/villager.png")

images = {
    "VILLAGER": {
        "RED": pygame.image.load("assets/VILLAGER_RED.png"),
        "MAGENTA": pygame.image.load("assets/VILLAGER_PURPLE.png"),
        "GREEN": pygame.image.load("assets/VILLAGER_GREEN.png"),
        "YELLOW": pygame.image.load("assets/VILLAGER_YELLOW.png"),
        "BLUE": pygame.image.load("assets/VILLAGER_BLUE.png"),
        "WHITE": pygame.image.load("assets/VILLAGER_BLACK.png"),
        "CYAN": pygame.image.load("assets/VILLAGER_TURQUOISE.png"),
    },
    "ARCHER": {
        "RED": pygame.image.load("assets/ARCHER_RED.png"),
        "MAGENTA": pygame.image.load("assets/ARCHER_PURPLE.png"),
        "GREEN": pygame.image.load("assets/ARCHER_GREEN.png"),
        "YELLOW": pygame.image.load("assets/ARCHER_YELLOW.png"),
        "BLUE": pygame.image.load("assets/ARCHER_BLUE.png"),
        "WHITE": pygame.image.load("assets/ARCHER_BLACK.png"),
        "CYAN": pygame.image.load("assets/ARCHER_TURQUOISE.png"),
    },
    "HORSEMAN": {
        "RED": pygame.image.load("assets/HORSEMAN_RED.png"),
        "MAGENTA": pygame.image.load("assets/HORSEMAN_PURPLE.png"),
        "GREEN": pygame.image.load("assets/HORSEMAN_GREEN.png"),
        "YELLOW": pygame.image.load("assets/HORSEMAN_YELLOW.png"),
        "BLUE": pygame.image.load("assets/HORSEMAN_BLUE.png"),
        "WHITE": pygame.image.load("assets/HORSEMAN_BLACK.png"),
        "CYAN": pygame.image.load("assets/HORSEMAN_TURQUOISE.png"),
    },
    "SWORDMEN": {
        "RED": pygame.image.load("assets/SWORDSMEN_RED.png"),
        "MAGENTA": pygame.image.load("assets/SWORDSMEN_PURPLE.png"),
        "GREEN": pygame.image.load("assets/SWORDSMEN_GREEN.png"),
        "YELLOW": pygame.image.load("assets/SWORDSMEN_YELLOW.png"),
        "BLUE": pygame.image.load("assets/SWORDSMEN_BLUE.png"),
        "WHITE": pygame.image.load("assets/SWORDSMEN_BLACK.png"),
        "CYAN": pygame.image.load("assets/SWORDSMEN_TURQUOISE.png"),
    },
}

class UnitSprite(Element):
    def __init__(self, unit, isometry):
        self.unit = unit
        if isinstance(unit, Villager):
            image = images["VILLAGER"][unit.get_player().get_color().upper()]
        elif isinstance(unit, Archer):
            image = images["ARCHER"][unit.get_player().get_color().upper()]
        elif isinstance(unit, Horseman):
            image = images["HORSEMAN"][unit.get_player().get_color().upper()]
        elif isinstance(unit, Swordsman):
            image = images["SWORDMEN"][unit.get_player().get_color().upper()]
        super().__init__(sprite_image=image, x=lambda: unit.get_position().get_x(), y=lambda: unit.get_position().get_y(), isometry=isometry)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        print("UnitSprite update")
        print(self.x(), self.y())
