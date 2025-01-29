from datetime import timedelta

from core import Map
from core.actions import Action
from core.buildings import Building
from core.buildings.archery_range import ArcheryRange
from core.buildings.barracks import Barracks
from core.buildings.stable import Stable
from core.buildings.town_center import TownCenter
from core.position import Position
from core.units.archer import Archer
from core.units.horse_man import Horseman
from core.units.swordsman import Swordsman
from core.units.villager import Villager


class TrainingAction(Action):

    __map: Map
    __building: Building
    __type_unit: type
    __training: bool

    def __init__(self, map: Map, building: Building, type_unit: type):
        self.__map = map
        if isinstance(building, TownCenter):
            assert type_unit == Villager
        elif isinstance(building, Barracks):
            assert type_unit == Swordsman
        elif isinstance(building, ArcheryRange):
            assert type_unit == Archer
        else:
            assert type_unit == Horseman and isinstance(building, Stable)
        self.__type_unit = type_unit
        self.__building = building
        self.__training = False
        super().__init__()
        if not (building.is_training()):
            self.__training = True
            building.train()
            self.after_action()

    def _is_valid_position(
        self, position: Position
    ) -> bool:  # fonction absolument volée à Charles
        if not (
            0 <= position.get_x() < self.__map.get_width()
            and 0 <= position.get_y() < self.__map.get_height()
        ):
            # print(f"Position {position} is out of map bounds.")
            return False

        for building in self.__map.get_buildings():
            if not building.is_walkable():
                if (
                    building.get_position().get_x()
                    <= position.get_x()
                    < building.get_position().get_x() + building.get_width()
                    and building.get_position().get_y()
                    <= position.get_y()
                    < building.get_position().get_y() + building.get_height()
                ):
                    # print(f"Position {position} collides with building at {building.get_position()}.")
                    return False

        # print(f"Position {position} is valid.")
        return True

    def do_action(self):

        if self.__training:

            self.before_action()
            p0 = Position(0, 0)

            # on veut récupérer le temps d'entrainement
            if self.__type_unit == Villager:
                u = Villager(self.__building.get_player(), p0)
            elif self.__type_unit == Swordsman:
                u = Swordsman(self.__building.get_player(), p0)
            elif self.__type_unit == Archer:
                u = Archer(self.__building.get_player(), p0)
            else:
                u = Horseman(self.__building.get_player(), p0)

            if (self.get_new_time() - self.get_old_time()) > timedelta(
                seconds=u.get_training_time()
            ):
                # calcul de la position
                valid_found = False
                n = 1  # n est la distance par rapport au building
                while not (valid_found or n > 10):
                    for i in range(n):
                        p = Position(n, i)
                        if self._is_valid_position(p):
                            valid_found = True
                        if not (valid_found):
                            for i in range(n):
                                p = Position(i, n)
                                if self._is_valid_position(p):
                                    valid_found = True
                    n += 1

                if valid_found:
                    true_p = self.__building.get_position()  # ce fut un placeholder
                    u.position = true_p
                    self.__map.add_unit(u)
                    self.__building.end_training()
                    return True
            return False

        else:
            if not (self.__building.is_training()):
                self.__training = True
                self.__building.train()
                self.after_action()
            return False

    def get_type_unit(self):
        return self.__type_unit