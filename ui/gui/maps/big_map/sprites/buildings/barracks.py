import pygame.image

from ui.gui.utils.camera import Camera
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.ressources import Resource

image = pygame.image.load("assets/barracks.png")
towncenters = {
    "RED": pygame.image.load("assets/BARRACKS_RED.png"),
    "BLUE": pygame.image.load("assets/BARRACKS_BLUE.png"),
    "GREEN": pygame.image.load("assets/BARRACKS_GREEN.png"),
    "YELLOW": pygame.image.load("assets/BARRACKS_YELLOW.png"),
    "MAGENTA": pygame.image.load("assets/BARRACKS_MAGENTA.png"),
    "CYAN": pygame.image.load("assets/BARRACKS_CYAN.png"),
    "WHITE": pygame.image.load("assets/BARRACKS_WHITE.png")
}
class BarracksSprite(Resource):

    def __init__(self, resource):
        super().__init__(resource, towncenters[resource.get_player().get_color()], Isometry(Camera.get_tile_length))

