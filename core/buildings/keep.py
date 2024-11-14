from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource



class Keep(Building):
    __damage : int
    __range : float
    __attack_speed : float

    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(35,125,0)
        self.__damage = 4
        self.__range = 4
        self.__attack_speed = 1
        super().__init__(80, 1, 800, position, 1, False, resource_cost, player)

    def get_damage(self):
        return self.__damage

    def get_range(self):
        return self.__range

    def get_attack_speed(self):
        return self.__attack_speed

p = Position(5, 6)
play = Player("Philip", "red")
f = Keep(p, play)
print(f.get_damage(), f.get_range(), f.get_attack_speed())