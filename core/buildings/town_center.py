from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource



class TownCenter(Building):


    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(350,0,0)
        super().__init__(150, 4, 1000, position, 4, False, resource_cost,player)

