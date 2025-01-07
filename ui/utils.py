import math
from core import Unit, Building
from core.position import Position


class Utils:
    @staticmethod
    def distance_between_two_positions(position1: Position, position2: Position):
        return math.sqrt((position1.get_x() - position2.get_x())**2 +(position1.get_y() - position2.get_y())**2 )

    @staticmethod
    def distance_between_two_units(unit1: Unit, unit2: Unit) -> float:
        return Utils.distance_between_two_positions(unit1.get_position(), unit2.get_position())

    @staticmethod
    def distance_between_position_and_units(position: Position, unit: Unit):
        return Utils.distance_between_two_positions(position, unit.get_position())

    @staticmethod
    def distance_between_unit_and_buildings(self, unit: Unit, building: Building):
        return min(Utils.distance_between_position_and_units(Position(x, y), unit)
                   for x in range(int(building.get_position().get_x()), int(building.get_position().get_x() + building.get_width()))
                   for y in range(int(building.get_position().get_y()), int(building.get_position().get_y() + building.get_height())))


    @staticmethod
    def distance_between_two_buildings(building1: Building, building2: Building):
        return min(Utils.distance_between_two_positions(Position(x1, y1), Position(x2, y2))
                   for x1 in range(int(building1.get_position().get_x()), int(building1.get_position().get_x() + building1.get_width()))
                   for y1 in range(int(building1.get_position().get_y()), int(building1.get_position().get_y() + building1.get_height()))
                     for x2 in range(int(building2.get_position().get_x()), int(building2.get_position().get_x() + building2.get_width()))
                     for y2 in range(int(building2.get_position().get_y()), int(building2.get_position().get_y() + building2.get_height())))
