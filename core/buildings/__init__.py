from core.players import Player
from core.position import Position
from core.resource import Resource
from core.utils import generate_id


class Building:
    __building_percent: float
    __build_time: float
    __height: int
    __health_points: int
    __max_health_points: int
    __player: Player
    __position: Position
    __width: int
    __walkable: bool
    __cost_resource: Resource
    __training: bool

    def __init__(
        self,
        build_time: float,
        height: int,
        health_point: int,
        position: Position,
        width: int,
        walkable: bool,
        cost_resource: Resource,
        player: Player,
    ):

        self.id = generate_id()
        self.__building_percent = 0
        assert width > 0 and height > 0
        self.__build_time = build_time
        self.__height = height
        self.__health_points = health_point
        self.__max_health_points = health_point
        self.__position = position
        self.__width = width
        self.__walkable = walkable
        self.__cost_resource = cost_resource
        self.__player = player
        self.__training = False

    def get_building_percent(self) -> float:
        return self.__building_percent

    def get_build_time(self) -> float:
        return self.__build_time

    def get_height(self) -> int:
        return self.__height

    def get_health_points(self) -> int:
        return self.__health_points

    def get_max_health_points(self) -> int:
        return self.__max_health_points

    def get_position(self) -> Position:
        return self.__position

    def get_width(self) -> int:
        return self.__width

    def is_walkable(self) -> bool:
        return self.__walkable

    def get_cost_resource(self) -> Resource:
        return self.__cost_resource

    def is_built(self) -> bool:
        return self.__building_percent >= 100

    def remove_health_points(self, value: int):
        assert value >= 0, value
        self.__health_points -= value

    def get_player(self) -> Player:
        return self.__player

    def build(self, value: float):
        assert value >= 0, value
        self.__building_percent += value
        print(f"Building {self.__building_percent}% complete.")

    def is_training(self) -> bool:
        return self.__training

    def train(self):
        self.__training = True

    def end_training(self):
        self.__training = False

    # def update() :

    def __setattr__(self, key, value):
        from network.sender import Sender
        from network.state import State

        super().__setattr__(key, value)
        #if not State.is_receiving() and key in ("max_number_units", "stock", "name", "color") and self.__class__.__name__ != "Player":
        if not State.is_receiving() and key not in ("id") and self.__class__.__name__ != "Player":
            Sender.notify_edit(self, key, value)
