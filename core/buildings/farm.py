from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource
from network.state import State


class Farm(Building):
    resources : Resource

    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(60,0,0)
        super().__init__(10, 2, 100, position, 2, True, resource_cost,player)

        old_state = State.is_receiving()
        State.set_receiving(True)
        self.resources = Resource(0,0,300) #
        State.set_receiving(old_state)



    def collect(self, food : int)  :
        old_food = self.resources.get_food()
        if old_food != 0 :
            new_food = old_food - food
            if new_food < 0 :
                self.resources.remove_food(old_food)
            else :
                self.resources.remove_food(food)

    def get_resource (self):
        return self.resources