from core.position import Position

from core.resource import Resource

from core.resources_points import ResourcePoint



class Mine(ResourcePoint) :
    def __init__(self, position : Position):
        ResourcePoint.__init__(self ,position,Resource(0,800 , 0))