import pygame.image

from ui.gui.maps.big_map.sprites.ressources import Resource

wood_image = pygame.image.load("assets/gold.png")

class MineSprite(Resource):

    def __init__(self, wood, isometry):
        super().__init__(wood, wood_image, isometry, 1)
