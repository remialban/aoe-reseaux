from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource



class Keep(Building):


    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(35,125,0)
        super().__init__(80, 1, 800, position, 1, False, resource_cost, player)

