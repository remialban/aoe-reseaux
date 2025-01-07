from abc import abstractmethod

import pygame.sprite

from ui.gui.utils.camera import Camera
from ui.gui.maps.big_map.sprites.ressources.wood import WoodSprite
from ui.gui.utils.isometry import Isometry


class Map:
    def __init__(self, tile_length: float, offset_x, offset_y, isometry: Isometry, screen):
        self.screen = screen
        self.isometry = isometry

        self.buildings = pygame.sprite.Group()
        self.resource_points = pygame.sprite.Group()
        self.units = pygame.sprite.Group()

        self.buildings_objects = set()
        self.units_objects = set()
        self.resource_points_objects = set()


        self.tile_length = tile_length
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.grass_list = pygame.sprite.Group()
        #self.grass_list.add(Grass(0,0, UIManager.get_game().get_map().get_width(), UIManager.get_game().get_map().get_height()))

        self.camera_position = Camera.get_x(), Camera.get_y()
        self.tile_cam = Camera.get_tile_length()

    @abstractmethod
    def add_building_sprite(self, building):
        pass

    @abstractmethod
    def add_unit_sprite(self, unit):
        pass

    @abstractmethod
    def add_resource_point_sprite(self, resource_point):
        self.resource_points.add(WoodSprite(resource_point))

    @abstractmethod
    def remove_building_sprite(self, building):
        pass

    def add_building(self, building):
        if building not in self.buildings_objects:
            self.buildings_objects.add(building)
            self.add_building_sprite(building)
        # if not any(b.resource == building for b in self.buildings):
        #     # Create sprite building and add
        #     self.add_building_sprite(building)

    def remove_building(self, building):
        building_to_remove = None
        self.buildings_objects.remove(building)
        for b in self.buildings:
            if b.resource == building:
                building_to_remove = b

        if building_to_remove is not None:
            self.buildings.remove(building_to_remove)

    def add_units(self, unit):
        if unit not in self.units_objects:
            self.units_objects.add(unit)
            self.add_unit_sprite(unit)

        # if not any(u.unit == unit for u in self.units):
        #     self.add_unit_sprite(unit)

    def remove_unit(self, unit):
        unit_to_remove = None
        self.units_objects.remove(unit)
        for u in self.units:
            if u.unit == unit:
                unit_to_remove = u

        if unit_to_remove is not None:
            self.units.remove(unit_to_remove)

    def add_resource_point(self, resource_point):
        if resource_point not in self.resource_points_objects:
            self.resource_points_objects.add(resource_point)
            self.add_resource_point_sprite(resource_point)
        # if not any(rp.resource == resource_point for rp in self.resource_points):
        #     self.add_resource_point_sprite(resource_point)

    def remove_resource_point(self, unit):
        resource_point_to_remove = None
        self.resource_points_objects.remove(unit)
        for rp in self.resource_points:
            if rp.unit == unit:
                building_to_remove = rp

        if resource_point_to_remove is not None:
            self.resource_points.remove(resource_point_to_remove)

    def draw(self):
        self.grass_list.draw(self.screen)
        for grass in self.grass_list:
            if self.screen.get_rect().colliderect(grass.rect):
                self.screen.blit(grass.image, grass.rect)

        for resource_point in self.resource_points:
            if self.screen.get_rect().colliderect(resource_point.rect):
                self.screen.blit(resource_point.image, resource_point.rect)

        for building in self.buildings:
            if self.screen.get_rect().colliderect(building.rect):
                self.screen.blit(building.image, building.rect)

        for unit in self.units:
            if self.screen.get_rect().colliderect(unit.rect):
                self.screen.blit(unit.image, unit.rect)

        # self.grass_list.draw(self.screen)
        # self.resource_points.draw(self.screen)
        # self.buildings.draw(self.screen)
        # self.units.draw(self.screen)


    def update(self):
        if self.tile_cam != Camera.get_tile_length() or self.camera_position != (Camera.get_x(), Camera.get_y()):
            self.tile_cam = Camera.get_tile_length()
            self.camera_position = Camera.get_x(), Camera.get_y()
        self.grass_list.update()
        self.resource_points.update()
        self.buildings.update()
        self.units.update()
