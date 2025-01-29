from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource
from core.units import Unit


class Camp(Building):


    def __init__(self, position : Position, player : Player):
        resource_cost = Resource(100,0,0)
        super().__init__(25, 2, 200, position, 2, False, resource_cost, player)

    def drop_off_resources(self, unit: Unit):
        unit_stock = unit.get_stock()
        converted = Resource(unit_stock["wood"], unit_stock["gold"], unit_stock["food"])
        self.player.add_resources(converted)
        unit.remove_resources("wood", converted.get_wood())
        unit.remove_resources("food", converted.get_food())
        unit.remove_resources("gold", converted.get_gold())