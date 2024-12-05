from enum import Enum
from core.players import Player
from core.buildings import Building
from core.buildings.town_center import TownCenter
from core.position import Position
from core.resources_points.mine import Mine
from core.resources_points.wood import Wood
from core.resources_points import ResourcePoint
from core.units import Unit
from random import randint
from core.units.villager import Villager
from math import sqrt, cos, sin
from math import radians

class Modes(Enum):
    GOLD_RUSH = 1
    GENEROUS = 2
    NORMAL = 3

class Map:
    min_distance_between_players = 0
    def __init__(self, width: int, height: int, mode: Modes, players: set) -> None:

        self.__width: int = width
        self.__height: int = height

        self.buildings: set[Building] = set()
        self.units: set[Unit] = set()
        self.resources_points: set[ResourcePoint] = set()

        Map.min_distance_between_players = max(2, int(min(self.__width, self.__height) * 0.5))

        if mode == Modes.NORMAL:
            self.initialize_players(players, mode)
            self.generate_resources(10, mode)
        elif mode == Modes.GOLD_RUSH:
            self.initialize_players(players, mode)
            self.generate_resources(1, mode)
        elif mode == Modes.GENEROUS:
            self.initialize_players(players, mode)
            self.generate_resources(30, mode)
        else:
            raise ValueError("Invalid mode")

    def generate_wood_clusters(self, num_clusters: int, cluster_range: int, max_wood_per_cluster: int) -> None:
        assert (2 * cluster_range + 1) ** 2 >= max_wood_per_cluster, "Cluster range is too small for the number of wood to generate"
        for _ in range(num_clusters):
            cluster_center = Position(randint(0, self.__width - 1), randint(0, self.__height - 1))
            for _ in range(max_wood_per_cluster):
                new_x = cluster_center.get_x() + randint(-cluster_range, cluster_range)
                new_y = cluster_center.get_y() + randint(-cluster_range, cluster_range)
                if 0 <= new_x < self.__width and 0 <= new_y < self.__height:
                    new_position = Position(new_x, new_y)
                    if self.check_resource_point_position(Wood(new_position)):
                        self.resources_points.add(Wood(new_position))

    def generate_resources(self, percentage: float, mode: Modes) -> None:
        assert 0 <= percentage <= 100, "Percentage must be between 0 and 100"

        map_area = self.__width * self.__height
        num_resources = int(map_area * (percentage / 100))
        num_each_resource = num_resources // 2

        if mode == Modes.GOLD_RUSH:
            center_x = self.__width // 2
            center_y = self.__height // 2
            max_radius = min(self.__width, self.__height) // 4  # Limit radius to keep resources focused

            resources_added = 0
            while resources_added < num_each_resource:

                angle = randint(0, 360)
                radius = randint(0, max_radius)
                offset_x = int(radius * cos(radians(angle)))
                offset_y = int(radius * sin(radians(angle)))

                mine_position = Position(center_x + offset_x, center_y + offset_y)
                mine = Mine(mine_position)

                if self.check_resource_point_position(mine):
                    self.resources_points.add(mine)
                    resources_added += 1

            resources_added = 0
            while resources_added < num_each_resource:
                self.generate_wood_clusters(1, 2, 5)
                resources_added += 1

        else:
            resources_added = 0
            while resources_added < num_each_resource:
                mine_position = Position(randint(0, self.__width - 1), randint(0, self.__height - 1))
                mine = Mine(mine_position)
                if self.check_resource_point_position(mine):
                    self.resources_points.add(mine)
                    resources_added += 1

            resources_added = 0
            while resources_added < num_each_resource:
                self.generate_wood_clusters(1, 2, 5)
                resources_added += 1


    def generate_building(self,building_type: type, player: Player, building_tmp: list[Building]=[]) -> Building:
        building_pos = Position(randint(0, self.__width - 1), randint(0, self.__height - 1))
        building = building_type(building_pos, player)
        for i in range(1000):
            building_pos.set_x(randint(0, self.__width - 1))
            building_pos.set_y(randint(0, self.__height - 1))
            if self.check_building_position(building,building_tmp):
                return building
        return None

    def generate_unit(self,unit_type: type, player: Player, building: Building, unit_tmp: list[Unit]=[]) -> Unit:
        unit_pos = Position(randint(0, self.__width - 1), randint(0, self.__height - 1))
        unit = unit_type(player, unit_pos)
        for i in range(1000):
            unit_pos.set_x(randint(0, self.__width - 1))
            unit_pos.set_y(randint(0, self.__height - 1))
            if self.check_unit_position(unit, building):
                return unit
        return None

    def distance_unit_to_building(self, unit: Unit, building: Building) -> float:
        return min(sqrt((x-unit.get_position().get_x()) ** 2 + (y-unit.get_position().get_y()) ** 2)
                   for x in range(building.get_position().get_x(), building.get_position().get_x() + building.get_width())
                   for y in range(building.get_position().get_y(), building.get_position().get_y() + building.get_height()))

    def initialize_players(self, players: set[Player], mode: Modes) -> None:
        max_distance_same_player = 1  # Maximum distance for the same player's town centers to be relatively close

        def distance(pos1, pos2):
            return sqrt((pos1.get_x() - pos2.get_x()) ** 2 + (pos1.get_y() - pos2.get_y()) ** 2)


        town_centers = []
        villagers = []
        for i in range(10000):
            for player in players:
                town_center= self.generate_building(TownCenter, player, town_centers)
                if town_center is not None:
                    town_centers.append(town_center)
            print(Map.min_distance_between_players)
            distances = [distance(t1.get_position(), t2.get_position()) >= Map.min_distance_between_players for t1 in town_centers for t2 in town_centers if t1 != t2]
            if all(distances)  and len(town_centers) == len(players):
                break
            else:
                town_centers.clear()
        if len(town_centers) != len(players):
            raise Exception("Could not generate town centers, Map is too small")
        for town_center in town_centers:
            self.add_building(town_center)
        for i in range(10000):
            for town_center in town_centers:
                villager = self.generate_unit(Villager, town_center.get_player(), town_center)
                if villager is not None:
                    villagers.append(villager)
            is_distance_good = [self.distance_unit_to_building(villager, town_center) <= 1 for villager in villagers for town_center in town_centers if villager.get_player() == town_center.get_player()]
            if all(is_distance_good) and len(villagers) == len(town_centers):
                break
            else:
                villagers.clear()
        if len(villagers) != len(town_centers):
            raise Exception("Could not generate villager, Map is too small")
        for villager in villagers:
            self.add_unit(villager)

    def is_position_occupied(self, position: Position) -> bool:
        # Check if the position overlaps with any building
        for building in self.buildings:
            b_pos = building.get_position()
            if (b_pos.get_x() <= position.get_x() < b_pos.get_x() + building.get_width() and
                    b_pos.get_y() <= position.get_y() < b_pos.get_y() + building.get_height()):
                return True

        # Check if the position overlaps with any resource
        for resource in self.resources_points:
            if position == resource.get_position():
                return True

        return False

    def check_building_position(self, building: Building,building_tmp: list[Building]=[]) -> bool:
        pos = building.get_position()
        if (pos.get_x() < 0 or pos.get_x() + building.get_width()-1 >= self.__width or
            pos.get_y() < 0 or pos.get_y() + building.get_height()-1 >= self.__height):
            return False

        for b in self.buildings:
            b_pos = b.get_position()
            if not (pos.get_x() + building.get_width() <= b_pos.get_x() or
                    pos.get_x() >= b_pos.get_x() + b.get_width() or
                    pos.get_y() + building.get_height() <= b_pos.get_y() or
                    pos.get_y() >= b_pos.get_y() + b.get_height()):
                return False
        for b in building_tmp:
            b_pos = b.get_position()
            if not (pos.get_x() + building.get_width() <= b_pos.get_x() or
                    pos.get_x() >= b_pos.get_x() + b.get_width() or
                    pos.get_y() + building.get_height() <= b_pos.get_y() or
                    pos.get_y() >= b_pos.get_y() + b.get_height()):
                return False
        return True

    def check_unit_position(self, unit: Unit, building: Building, unit_tmp: list[Unit]=[]) -> bool:
        pos = unit.get_position() #check that unit is within map border
        if (pos.get_x() < 0 or pos.get_x() >= self.__width or
                pos.get_y() < 0 or pos.get_y() >= self.__height):
            return False

        for u in unit_tmp: #check that unit is not on top of another unit
            u_pos = u.get_position()
            if pos.get_x() == u_pos.get_x() and pos.get_y() == u_pos.get_y():
                return False

        for u in self.units:
            u_pos = u.get_position()
            if pos.get_x() == u_pos.get_x() and pos.get_y() == u_pos.get_y():
                return False

        for b in self.buildings: #check that unit is not on top of a building
            b_pos = b.get_position()
            if (b_pos.get_x() <= pos.get_x() < b_pos.get_x() + b.get_width() and
                    b_pos.get_y() <= pos.get_y() < b_pos.get_y() + b.get_height()):
                return False

        b_pos = building.get_position() #check that unit is not too far from the building
        if not (b_pos.get_x() - 1 <= pos.get_x() <= b_pos.get_x() + building.get_width() + 1 and
                b_pos.get_y() - 1 <= pos.get_y() <= b_pos.get_y() + building.get_height() + 1):
            return False

        return True

    def check_resource_point_position(self, resource_point: ResourcePoint) -> bool:
        pos = resource_point.get_position()
        if pos.get_x() < 0 or pos.get_x() >= self.__width or pos.get_y() < 0 or pos.get_y() >= self.__height:
            return False

        for rp in self.resources_points:
            if pos == rp.get_position():
                return False

        for unit in self.units:
            if pos == unit.get_position():
                return False

        for building in self.buildings:
            b_pos = building.get_position()
            if b_pos.get_x() <= pos.get_x() < b_pos.get_x() + building.get_width() and b_pos.get_y() <= pos.get_y() < b_pos.get_y() + building.get_height():
                return False

        return True

    def revalidate_resources(self):
        """Remove resources that overlap with buildings."""
        resources_to_remove = []
        for resource in self.resources_points:
            if self.is_position_occupied(resource.get_position()):
                resources_to_remove.append(resource)

        for resource in resources_to_remove:
            self.resources_points.remove(resource)

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def add_building(self, building: Building) -> None:
        self.buildings.add(building)

    def remove_building(self, building: Building) -> None:
        if building in self.buildings:
            self.buildings.remove(building)

    def add_unit(self, unit: Unit) -> None:
        self.units.add(unit)

    def remove_unit(self, unit: Unit) -> None:
        if unit in self.units:
            self.units.remove(unit)

    def get_units(self, player: object = None) -> set[Unit]:
        if player:
            return {unit for unit in self.units if unit.player == player}
        return self.units

    def get_buildings(self, player: object = None) -> set[Building]:
        if player:
            return {building for building in self.buildings if building.get_player() == player}
        return self.buildings

    def get_resources(self) -> set:
        return self.resources_points

    def clean (self):
        for building in self.buildings:
            if building.get_health_points() <= 0:
                self.buildings.remove(building)
        for unit in self.units:
            if unit.health_points <= 0:
                self.units.remove(unit)
        for resource_point in self.resources_points:
            resource = resource_point.get_resources()
            if resource.get_gold() + resource.get_wood() + resource.get_food()  <= 0:
                self.resources_points.remove(resource_point)