from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource
from core.units import Unit


class TownCenter(Building):


    def __init__(self, position : Position, player : Player):
        super().__init__(150, 4, 1000, position, 4, False, Resource(350,0,0),player)
        self.player = player

    def drop_off_resources(self, unit: Unit):
        unit_stock = unit.get_stock()
        converted = Resource(unit_stock["wood"], unit_stock["gold"], unit_stock["food"])
        self.player.add_resources(converted)
        unit.remove_resources("wood", converted.get_wood())
        unit.remove_resources("food", converted.get_food())
        unit.remove_resources("gold", converted.get_gold())
