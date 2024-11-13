import math
from datetime import timedelta

from core.actions import Action
from core.buildings import Building
from core.units import Unit


class AttackBuildingAction(Action):

    __attacking_unit : Unit
    __attacked_building : Building

    def __init__(self, attacking_unit : Unit, attacked_building : Building):
        self.__attacking_unit = attacking_unit
        self.__attacked_building = attacked_building
        super().__init__()




    def do_action(self)->bool:
        if (math.sqrt((self.__attacked_building.get_position().get_x() - self.__attacking_unit.get_position().get_x())*(self.__attacked_building.get_position().get_x() - self.__attacking_unit.get_position().get_x()) +(self.__attacked_building.get_position().get_y() -self.__attacking_unit.get_position().get_y())*(self.__attacked_building.get_position().get_y() -self.__attacking_unit.get_position().get_y()) )<= self.__attacking_unit.range):
            if ((self.get_new_time() - self.get_old_time()) > timedelta(seconds = self.__attacking_unit.attack_speed)):
                self.__attacked_building.remove_health_points(self.__attacking_unit.damage)

        return True
