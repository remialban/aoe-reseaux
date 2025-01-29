import math
from datetime import timedelta

from core.actions import Action
from core.buildings.keep import Keep
from core.units import Unit


class AttackUnitByBuildingAction(Action):

    __attacking_keep: Keep
    __attacked_unit: Unit

    def __init__(self, attacking_keep: Keep, attacked_unit: Unit):
        self.__attacking_keep = attacking_keep
        self.__attacked_unit = attacked_unit
        super().__init__()

    def do_action(self) -> bool:

        self.before_action()

        if self.__attacking_keep.get_health_points() <= 0:
            return True

        distance_x = (
            self.__attacked_unit.get_position().get_x()
            - self.__attacking_keep.get_position().get_x()
        )
        distance_y = (
            self.__attacked_unit.get_position().get_y()
            - self.__attacking_keep.get_position().get_y()
        )
        if (
            math.sqrt(distance_x**2 + distance_y**2)
            <= self.__attacking_keep.get_range()
        ):
            if (self.get_new_time() - self.get_old_time()) > timedelta(
                seconds=self.__attacking_keep.get_attack_speed()
            ):
                self.__attacked_unit.remove_health_points(
                    self.__attacking_keep.get_damage()
                )
                self.after_action()

        return self.__attacked_unit.get_health_points() <= 0
