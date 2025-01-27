import math

import pygame

from core.buildings.archery_range import ArcheryRange
from core.buildings.barracks import Barracks
from core.buildings.camp import Camp
from core.buildings.farm import Farm
from core.buildings.keep import Keep
from core.buildings.stable import Stable
from core.buildings.town_center import TownCenter
from core.resources_points.wood import Wood
from ui.gui.maps.big_map.sprites.buildings.archery_range import ArcheryRangeSprite
from ui.gui.maps.big_map.sprites.buildings.barracks import BarracksSprite
from ui.gui.maps.big_map.sprites.buildings.farm import FarmSprite
from ui.gui.maps.big_map.sprites.buildings.keep import KeepSprite
from ui.gui.maps.big_map.sprites.buildings.stable import StableSprite
from ui.gui.maps.big_map.sprites.ressources.mine import MineSprite
from ui.gui.maps.minimap.sprites.building import BuildingSprite
from ui.gui.maps.minimap.sprites.resource_point import ResourcePointSprite
from ui.gui.minimap.grass import Grass
# from ui.gui.maps.big_map.sprites.ressources import MineSprite
from ui.gui.maps.big_map.sprites.buildings.camp import CampSprite
from ui.gui.maps.big_map.sprites.buildings.town_center import TownCenterSprite
from ui.gui.maps.big_map.sprites.ressources.wood import WoodSprite
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.map import Map
from math import cos, radians

from ui.ui_manager import UIManager


class MiniMap(Map):
    def __init__(self, tile_length, offset_x, offset_y, screen):
        # calcul_tile_length = 100 * cos(radians(60)) / (UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height())
        calcul_tile_length = 300 / (cos(radians(60)) * (UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height()))
        super().__init__(calcul_tile_length, UIManager.get_game().get_map().get_width(), 0, Isometry(tile_length=lambda: calcul_tile_length), screen)
        width, height = screen.get_size()
        self.generate_grass_image(calcul_tile_length)
        self.grass_list.add(Grass(UIManager.get_game().get_map().get_width() - 1, UIManager.get_game().get_map().get_height() - 1, 100, calcul_tile_length))
        # self.grass_list.add(Grass(0, 0, 100, calcul_tile_length))

        print("Calcul : ",calcul_tile_length)

    def generate_grass_image(self, tile_len):
        # Colors
        white = (255, 255, 255, 0)  # Transparent background
        blue = (0, 100, 0)


        # Function to calculate vertices of a parallelogram
        def calculate_parallelogram(x, y, base, height, angle_deg):
            base*=tile_len
            height*=tile_len
            angle_rad = math.radians(angle_deg)
            dx = height / math.tan(angle_rad)

            width_image = cos(radians(30)) * (base + height)
            height_image = math.cos(radians(60)) * (base + height)

            self.minimap_width = width_image
            self.minimap_height = height_image

            return [
                (cos(radians(30)) * height, 0),
                (width_image, math.cos(radians(60)) * base),
                (math.cos(radians(30)) * base, height_image),
                (0, cos(radians(60)) * height)

            ]
            bottom_left = (x, y)
            bottom_right = (x + base, y)
            top_right = (x + base - dx, y - height)
            top_left = (x - dx, y - height)

            return [bottom_left, bottom_right, top_right, top_left]

        # Parameters for the parallelogram
        base_length = UIManager.get_game().get_map().get_width()
        parallelogram_height = UIManager.get_game().get_map().get_height()
        angle_degrees = 120

        # Calculate vertices relative to (0, 0)
        vertices = calculate_parallelogram(0, parallelogram_height, base_length, parallelogram_height, angle_degrees)
        print(vertices)

        # Determine the bounding box
        min_x = min(v[0] for v in vertices)
        max_x = max(v[0] for v in vertices)
        min_y = min(v[1] for v in vertices)
        max_y = max(v[1] for v in vertices)

        # Adjust vertices to fit in a minimal bounding box
        adjusted_vertices = [(x - min_x, y - min_y) for x, y in vertices]

        # Create a surface with the size of the bounding box
        surface_width = int(max_x - min_x)
        surface_height = int(max_y - min_y)
        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)

        # Fill the background with transparency
        surface.fill(white)

        # Draw the parallelogram on the surface
        pygame.draw.polygon(surface, blue, adjusted_vertices)

        # Save the surface as an image file
        pygame.image.save(surface, "grass.png")

    def add_resource_point_sprite(self, resource_point):
        self.resource_points.add(ResourcePointSprite(resource_point, self.isometry))
        return None
        match resource_point:
            case Wood():
                self.resource_points.add(ResourcePointSprite(resource_point, self.isometry))
            case _:
                self.resource_points.add(MineSprite(resource_point, self.isometry))

    def add_building_sprite(self, building):
        self.buildings.add(BuildingSprite(building, self.isometry))
        return None
        match building:
            case TownCenter():
                self.buildings.add(TownCenterSprite(building))
            case ArcheryRange():
                self.buildings.add(ArcheryRangeSprite(building))
            case Barracks():
                self.buildings.add(BarracksSprite(building))
            case Camp():
                self.buildings.add(CampSprite(building))
            case Keep():
                self.buildings.add(KeepSprite(building))
            case Farm():
                self.buildings.add(FarmSprite(building))
            case Stable():
                self.buildings.add(StableSprite(building))
            case _:
                pass
        self.buildings.add(TownCenterSprite(building))

    def draw(self):
        super().draw()

