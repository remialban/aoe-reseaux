import pygame.image

from ui.gui.utils.camera import Camera
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.ressources import Resource

town_center_image = pygame.image.load("assets/house.png")

town_centers = {
    "RED": pygame.image.load("assets/HOUSE_RED.png"),
    "BLUE": pygame.image.load("assets/HOUSE_BLUE.png"),
    "GREEN": pygame.image.load("assets/HOUSE_GREEN.png"),
    "YELLOW": pygame.image.load("assets/HOUSE_YELLOW.png"),
    "MAGENTA": pygame.image.load("assets/HOUSE_MAGENTA.png"),
    "CYAN": pygame.image.load("assets/HOUSE_CYAN.png"),
    "WHITE": pygame.image.load("assets/HOUSE_WHITE.png")
}

class HouseSprite(Resource):

    def __init__(self, resource):
        super().__init__(resource, town_centers[resource.get_player().get_color()], Isometry(Camera.get_tile_length))

