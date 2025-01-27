import pygame.image

from core.actions.attack_building_action import AttackBuildingAction
from core.actions.attack_unit_action import AttackUnitAction
from core.actions.collect_action import Collect_Action
from core.units.archer import Archer
from core.units.horse_man import Horseman
from core.units.swordsman import Swordsman
from core.units.villager import Villager
from ui.gui.maps.big_map.sprites.element import Element
from ui.ui_manager import UIManager


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

    def draw(self, screen):
        #super(self).s

        # if self.rect.midright[0] < 0 or self.rect.midleft[0] > screen.get_width() or self.rect.midbottom[1] < 0 or self.rect.midtop[1] > screen.get_height():
        #     return

        actions = UIManager.get_game().get_actions()


        isAttackingUnit = any(isinstance(a, AttackUnitAction) and a.get_attacking_unit() == self.unit for a in actions)
        isAttackingBuilding = any(isinstance(a, AttackBuildingAction) and a.get_attacking_unit() == self.unit for a in actions)

        if isinstance(self.unit, Villager):
            isCollecting = any(isinstance(a, Collect_Action) and a.get_villager() == self.unit for a in actions)
        else:
            isCollecting = False

        isAttacked = any(isinstance(a, AttackUnitAction) and a.get_attacked_unit() == self.unit for a in actions)
        font = pygame.font.Font(pygame.font.get_default_font(), 12 * self.image.get_height() // 50)

        h1 = 0
        if isAttacked:
            text1 = f"HP: {self.unit.get_health_points()}/100"
            text_surface = font.render(text1, True, (255, 255, 255))
            rect = text_surface.get_rect()
            h1 = rect.height
            rect.midbottom= self.rect.midtop
            screen.blit(text_surface, rect)

        text2 = ""
        if isAttackingUnit:
            text2 = "En attaque joueur"
        elif isAttackingBuilding:
            text2 = "En attaque bâtiment"
        elif isCollecting:
            text2 = "En collecte"

        text_surface = font.render(text2, True, (255, 255, 255))
        rect = text_surface.get_rect()
        rect.midbottom = self.rect.midtop
        rect.y -= h1
        h1 += rect.height
        screen.blit(text_surface, rect)


        resource = self.unit.get_stock()
        if isCollecting:
            text3 = f"W: {resource.get('wood')} F: {resource.get('food')} G: {resource.get('gold')}"
            text_surface = font.render(text3, True, (255, 255, 255))
            rect = text_surface.get_rect()
            rect.midbottom = self.rect.midtop
            rect.y -= h1
            screen.blit(text_surface, rect)
