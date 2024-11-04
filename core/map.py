from core.buildings import Building
from core.resource import Resource
from core.units import Unit


class Map:
    def __init__(self, width: int, height: int):
        # Initialize the map with given width and height
        self.__width: int = width
        self.__height: int = height
        # Lists to store buildings, units, and resources on the map
        self.buildings: set[Building] = set()
        self.units: set[Unit] = set()
        self.resources: set[Resource] = set()


    def get_width(self) -> int:
        # Return the width of the map
        return self.__width

    def get_height(self) -> int:
        # Return the height of the map
        return self.__height

    def add_building(self, building: Building) -> None:
        # Add a building to the list of buildings
        self.buildings.add(building)

    def remove_building(self, building: Building) -> None:
        # Remove a building from the list of buildings if it exists
        if building in self.buildings:
            self.buildings.remove(building)

    def add_unit(self, unit: object) -> None:
        # Add a unit to the list of units
        self.units.add(unit)

    def remove_unit(self, unit: object) -> None:
        # Remove a unit from the list of units if it exists
        if unit in self.units:
            self.units.remove(unit)

    def get_units(self, player: object = None) -> set[Unit]:
        # Return all units, or filter by player if specified
        if player:
            return {unit for unit in self.units if unit.player == player}
        return self.units

    def get_buildings(self, player: object = None) -> set:
        # Return all buildings, or filter by player if specified
        if player:
            return {building for building in self.buildings if building.get_player() == player}
        return self.buildings

    def get_resources(self) -> set:
        # Return the list of resources
        return self.resources

