from core.buildings import Building
from core.position import Position
from core.resource import Resource



class Farm(Building):
    resources : Resource

    def __init__(self, position : Position):
        self.resources = Resource(0,0,300) #
        resource_cost = Resource(60,0,0)
        super().__init__(10, 2, 100, position, 2, True, resource_cost)



    def collect(self, food : int)  :
        old_food = self.resources.get_food()
        if old_food != 0 :
            new_food = old_food - food
            if new_food < 0 :
                self.resources.remove_food(old_food)
            else :
                self.resources.remove_food(food)

