from core import Action
from core.buildings.farm import Farm
from core.resource import Resource
from core.resources_points import ResourcePoint
from core.resources_points.wood import Wood
from core.resources_points.mine import Mine
from core.units.villager import Villager



class Collect_Action(Action):

    __villager : Villager
    __collected : ResourcePoint
    __void :Resource

    def __init__(self, villager: Villager, collected: ResourcePoint or Farm):
        super().__init__()
        self.__villager = villager
        self.__collected = collected
        self.__void =Resource(0,0,0)
        for key in self.__villager.get_stock():
            if key == "wood":
                self.__void.add_wood(self.__villager.get_stock()["wood"])
            elif key == "gold":
                self.__void.add_gold(self.__villager.get_stock()["gold"])
            elif key == "food":
                self.__void.add_food(self.__villager.get_stock()["food"])

    def do_action(self):

        if isinstance(self.__collected, ResourcePoint):

            if isinstance(self.__collected,Mine) :
                self.__collected.collect(10, self.__villager.get_max_stock(), self.__void)
                self.__villager.collect_resources("gold", 10)
                return 7

            elif isinstance(self.__collected,Wood):
                self.__collected.collect(10, self.__villager.get_max_stock(), self.__void)
                self.__villager.collect_resources("wood", 10)
                return 5

        elif isinstance(self.__collected,Farm):
            self.__collected.collect(10)
            self.__villager.collect_resources("food", 10)
            return 2

        else:
            return 0
    def get_resource(self):
        return self.__void

    def get_ptresource(self):
        return self.__collected

