import pygame.image

from ui.gui.utils.camera import Camera
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.ressources import Resource

town_center_image = pygame.image.load("assets/keep.png")
class KeepSprite(Resource):

    def __init__(self, resource):
        super().__init__(resource, town_center_image, Isometry(Camera.get_tile_length))

