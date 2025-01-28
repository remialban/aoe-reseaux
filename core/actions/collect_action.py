from datetime import timedelta

from core import Action
from core.buildings.farm import Farm
from core.resource import Resource
from core.resources_points import ResourcePoint
from core.resources_points.wood import Wood
from core.resources_points.mine import Mine
from core.units.villager import Villager

# SPEED = 0.46666666666666666666667  # 25 per minute
SPEED = 20

class Collect_Action(Action):
    __collected: ResourcePoint
    __void: Resource

    def __init__(self, villager: Villager, collected: ResourcePoint | Farm):
        self.set_involved_units(set([villager]))
        self.__collected = collected
        self.__void = Resource(0, 0, 0)
        for key in next(iter(self.get_involved_units())).get_stock():
            if key == "wood":
                self.__void.add_wood(
                    next(iter(self.get_involved_units())).get_stock()["wood"]
                )
            elif key == "gold":
                self.__void.add_gold(
                    next(iter(self.get_involved_units())).get_stock()["gold"]
                )
            elif key == "food":
                self.__void.add_food(
                    next(iter(self.get_involved_units())).get_stock()["food"]
                )
        super().__init__()

    def do_action(self):
        self.before_action()

        if (self.get_new_time() - self.get_old_time()) > timedelta(seconds=1):
            if (
                isinstance(self.__collected, Farm)
                and self.__collected.get_health_points() <= 0
            ):
                return True
            if isinstance(self.__collected, ResourcePoint) and (
                self.__void.get_wood() + self.__void.get_food() + self.__void.get_gold()
                < 20
            ):

                if isinstance(self.__collected, Mine):
                    self.__collected.collect(
                        SPEED,
                        next(iter(self.get_involved_units())).get_max_stock(),
                        self.__void,
                    )
                    next(iter(self.get_involved_units())).collect_resources(
                        "gold",
                        SPEED,
                    )
                    self.__void.add_gold(SPEED)
                    self.after_action()

                elif isinstance(self.__collected, Wood):
                    self.__collected.collect(
                        SPEED,
                        next(iter(self.get_involved_units())).get_max_stock(),
                        self.__void,
                    )
                    next(iter(self.get_involved_units())).collect_resources(
                        "wood",
                        SPEED,
                    )
                    self.__void.add_wood(SPEED)
                    self.after_action()

            elif (
                isinstance(self.__collected, Farm)
                and (
                    self.__void.get_wood()
                    + self.__void.get_food()
                    + self.__void.get_gold()
                    < 20
                )
                and (self.__collected.get_health_points() > 0)
            ):
                self.__void.add_food(SPEED)
                self.__collected.collect(SPEED)
                next(iter(self.get_involved_units())).collect_resources("food", SPEED)
                self.after_action()

            elif (
                self.__void.get_wood() + self.__void.get_food() + self.__void.get_gold()
                >= 20
                or self.__collected.get_resource() == Resource(0, 0, 0)
            ):
                return True

            else:
                return False

    def get_resource(self):
        return self.__void

    def get_ptresource(self):
        return self.__collected

    def get_villager(self):
        return next(iter(self.get_involved_units()))
