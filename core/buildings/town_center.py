from core.buildings import Building
from core.position import Position
from core.resource import Resource



class TownCenter(Building):


    def __init__(self, build_time :float, height :int, health_point : int, position : Position, width :int, walkable : bool, cost_resource : Resource):
        super().__init__(build_time, height, health_point, position, width, walkable, cost_resource)

