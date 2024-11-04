from core.players import Player
from core.position import Position
from core.resource import Resource


class Building :
    __building_percent : float
    __build_time : float
    __height : int
    __health_points : int
    __player : Player
    __position : Position
    __width : int
    __walkable : bool
    __cost_resource : Resource




    def __init__(self, build_time :float, height :int, health_point : int, position : Position, width :int, walkable : bool, cost_resource : Resource) :
        self.__building_percent =  0
        assert width >0 and height >0
        self.__build_time = build_time
        self.__height = height
        self.__health_points = health_point
        self.__position = position
        self.__width = width
        self.__walkable = walkable
        self.__cost_resource = cost_resource


    def get_building_percent(self) -> float:
        return self.__building_percent

    def get_build_time(self) -> float:
        return self.__build_time

    def get_height(self) -> int:
        return self.__height

    def get_health_point(self) -> int:
        return self.__health_points

    def get_position(self) -> Position :
        return self.__position

    def get_width(self)-> int:
        return self.__width

    def is_walkable(self)->bool:
        return self.__walkable

    def get_cost_resource(self)->Resource:
        return self.__cost_resource

    def is_built(self)->bool:
        return self.__building_percent >=100

    def remove_health_point(self, value : int):
        assert value >= 0, value
        self.__health_points -= value


    def get_player(self)->Player:
        return self.__player


    # def update() :


















