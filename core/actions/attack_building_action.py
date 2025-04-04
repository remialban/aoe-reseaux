import math
from datetime import timedelta

from core.actions import Action
from core.buildings import Building
from core.position import Position
from core.units import Unit


class AttackBuildingAction(Action):

    __attacking_unit: Unit
    __attacked_building: Building

    def __init__(self, attacking_unit: Unit, attacked_building: Building):
        self.__attacking_unit = attacking_unit
        self.__attacked_building = attacked_building
        super().__init__()

    def distance_between_position_and_units(self, position: Position, unit: Unit):
        return math.sqrt(
            (unit.get_position().get_x() - position.get_x()) ** 2
            + (unit.get_position().get_y() - position.get_y()) ** 2
        )

    def distance(self):
        return min(
            self.distance_between_position_and_units(
                Position(x, y), self.__attacking_unit
            )
            for x in range(
                int(self.__attacked_building.get_position().get_x()),
                int(
                    self.__attacked_building.get_position().get_x()
                    + self.__attacked_building.get_width()
                ),
            )
            for y in range(
                int(self.__attacked_building.get_position().get_y()),
                int(
                    self.__attacked_building.get_position().get_y()
                    + self.__attacked_building.get_height()
                ),
            )
        )

    def get_attacking_unit(self):
        return self.__attacking_unit

    def get_attacked_building(self):
        return self.__attacked_building

    def do_action(self) -> bool:
        self.before_action()
        print("In range of building", self.distance(), self.__attacking_unit.range)
        if self.distance() <= self.__attacking_unit.range:
            if (self.get_new_time() - self.get_old_time()) > timedelta(
                seconds=self.__attacking_unit.attack_speed
            ):
                print("Attacking building")
                self.__attacked_building.remove_health_points(
                    self.__attacking_unit.get_damage()
                )
                print("Damage", self.__attacking_unit.get_damage())
                print("Building health points", self.__attacked_building.get_health_points(), "/", self.__attacked_building.get_max_health_points())
                self.after_action()

        return self.__attacked_building.get_health_points() <= 0


    def get_list_attributes(self):
        return [[self.__attacked_building.id, "health_points","building"]]
