import pygame.image

from ui.gui.utils.camera import Camera
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.ressources import Resource

towncenters = {
    "RED": pygame.image.load("assets/TOWN_CENTER_RED.png"),
    "BLUE": pygame.image.load("assets/TOWN_CENTER_BLUE.png"),
    "GREEN": pygame.image.load("assets/TOWN_CENTER_GREEN.png"),
    "YELLOW": pygame.image.load("assets/TOWN_CENTER_YELLOW.png"),
    "MAGENTA": pygame.image.load("assets/TOWN_CENTER_MAGENTA.png"),
    "CYAN": pygame.image.load("assets/TOWN_CENTER_CYAN.png"),
    "WHITE": pygame.image.load("assets/TOWN_CENTER_WHITE.png")
}
town_center_image = pygame.image.load("assets/town_center3.png")
class TownCenterSprite(Resource):

    def __init__(self, towncenter):
        super().__init__(towncenter, towncenters[towncenter.get_player().get_color()], Isometry(Camera.get_tile_length))

