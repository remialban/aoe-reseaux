from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource



class Camp(Building):


    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(100,0,0)
        super().__init__(25, 2, 200, position, 2, False, resource_cost, player)

