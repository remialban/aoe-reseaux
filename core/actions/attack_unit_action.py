from core.actions import Action
from core.units import Unit
import math
from datetime import datetime, timedelta


class AttackUnitAction(Action):

    __attacking_unit : Unit
    __attacked_unit : Unit

    def __init__(self, attacking_unit : Unit, attacked_unit : Unit):
        self.__attacking_unit = attacking_unit
        self.__attacked_unit = attacked_unit
        super().__init__()


    def do_action(self)->bool:
        if (math.sqrt((self.__attacked_unit.get_position().get_x() - self.__attacking_unit.get_position().get_x())*(self.__attacked_unit.get_position().get_x() - self.__attacking_unit.get_position().get_x()) +(self.__attacked_unit.get_position().get_y() -self.__attacking_unit.get_position().get_y())*(self.__attacked_unit.get_position().get_y() -self.__attacking_unit.get_position().get_y()) )<= self.__attacking_unit.range):
            if ((self.get_new_time() - self.get_old_time()) > timedelta(seconds=self.__attacking_unit.attack_speed)):
                self.__attacked_unit.remove_health_points(self.__attacking_unit.get_damage())

        return True
