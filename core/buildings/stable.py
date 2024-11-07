from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource



class Stable(Building):


    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(175,0,0)
        super().__init__(50, 3, 500, position, 3, False, resource_cost, player)

