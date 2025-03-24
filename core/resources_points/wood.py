from core.position import Position

from core.resource import Resource

from core.resources_points import ResourcePoint



class Wood(ResourcePoint) :
    def __init__(self, position : Position,owner):
        ResourcePoint.__init__(self ,position,Resource(100,0 , 0),owner)