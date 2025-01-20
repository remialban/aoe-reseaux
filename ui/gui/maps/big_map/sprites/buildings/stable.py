import pygame.image

from ui.gui.utils.camera import Camera
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.ressources import Resource

town_center_image = pygame.image.load("assets/stable.png")

town_centers = {
    "RED": pygame.image.load("assets/STABLE_RED.png"),
    "BLUE": pygame.image.load("assets/STABLE_BLUE.png"),
    "GREEN": pygame.image.load("assets/STABLE_GREEN.png"),
    "MAGENTA": pygame.image.load("assets/STABLE_MAGENTA.png"),
    "CYAN": pygame.image.load("assets/STABLE_CYAN.png"),
    "WHITE": pygame.image.load("assets/STABLE_WHITE.png"),
    "YELLOW": pygame.image.load("assets/STABLE_YELLOW.png")
}
class StableSprite(Resource):

    def __init__(self, resource):
        super().__init__(resource, town_centers[resource.get_player().get_color()], Isometry(Camera.get_tile_length))

