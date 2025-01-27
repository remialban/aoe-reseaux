from core import Map, Player
from core.actions import Action
from core.buildings import Building
from core.buildings.archery_range import ArcheryRange
from core.buildings.barracks import Barracks
from core.buildings.camp import Camp
from core.buildings.farm import Farm
from core.buildings.house import House
from core.buildings.keep import Keep
from core.buildings.stable import Stable
from core.buildings.town_center import TownCenter
from core.position import Position


class CreateBuildingAction(Action):

    __map : Map
    __type_building : type
    __player : Player
    __position : Position

    def __init__(self, map: Map, type_building: type):
        self.__map : Map
        self.__player : Player
        self.__type_building = type_building
        self.__position : Position
        super().__init__()


    def _is_valid_position(self, position: Position) -> bool:  # fonction absolument volée à Charles
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

        p0 = Position(0,0)
        if self.__type_building == TownCenter:
                b = TownCenter(p0,self.__player )
        elif self.__type_building == House:
                b = House(p0,self.__player)
        elif self.__type_building == Camp:
                b = Camp(p0,self.__player)
        elif self.__type_building == Farm:
                b = Farm(p0,self.__player)
        elif self.__type_building == Keep:
                b = Keep(p0,self.__player)
        elif self.__type_building == Barracks:
                b = Barracks(p0,self.__player)
        elif self.__type_building == ArcheryRange:
                b = ArcheryRange(p0,self.__player)
        else :
            assert self.__type_building == Stable
            b = Stable(p0,self.__player)

        all_free = True

        for i in range (int(self.__position.get_x()),int(self.__position.get_x())+ b.get_width()):
            for j in range(int(self.__position.get_y()),int(self.__position.get_y())+ b.get_height()):
                if not(self._is_valid_position(self.__position)):
                    all_free = False

        if all_free :
            b.__position = self.__position
            self.__map.add_building(b)

        return True