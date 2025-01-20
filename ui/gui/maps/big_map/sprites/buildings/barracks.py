import pygame.image

from ui.gui.utils.camera import Camera
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.ressources import Resource

image = pygame.image.load("assets/barracks.png")

class BarracksSprite(Resource):

    def __init__(self, resource):
        super().__init__(resource, image, Isometry(Camera.get_tile_length))

