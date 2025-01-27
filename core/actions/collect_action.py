from datetime import timedelta

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
        self.before_action()
        if (self.get_new_time() - self.get_old_time()) > timedelta(seconds = 1):
            if isinstance(self.__collected, ResourcePoint) and (self.__void.get_wood() + self.__void.get_food() + self.__void.get_gold() < 20):

                if isinstance(self.__collected, Mine):
                    self.__collected.collect(0.46666666666666666666667, self.__villager.get_max_stock(), self.__void)
                    self.__villager.collect_resources("gold", 0.46666666666666666666667)
                    self.after_action()


                elif isinstance(self.__collected, Wood):
                    self.__collected.collect(5, self.__villager.get_max_stock(), self.__void)
                    self.__villager.collect_resources("wood", 0.46666666666666666666667)
                    self.after_action()


            elif isinstance(self.__collected, Farm) and (self.__void.get_wood() + self.__void.get_food() + self.__void.get_gold() < 20):
                self.__void.add_food(0.46666666666666666666667)
                self.__collected.collect(0.46666666666666666666667)
                self.__villager.collect_resources("food", 0.46666666666666666666667)
                self.after_action()

            elif self.__void.get_wood() + self.__void.get_food() + self.__void.get_gold() >= 20 or self.__collected.get_resource() == Resource(0, 0, 0):
                return True
            else:
                return False
    def get_resource(self):
        return self.__void

    def get_ptresource(self):
        return self.__collected

    def get_villager(self):
        return self.__villager

