from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource



class Keep(Building):
    damage : int
    range : float
    attack_speed : float

    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(35,125,0)
        self.damage = 4
        self.range = 4
        self.attack_speed = 1
        super().__init__(80, 1, 800, position, 1, False, resource_cost, player)

    def get_damage(self):
        return self.damage

    def get_range(self):
        return self.range

    def get_attack_speed(self):
        return self.attack_speed