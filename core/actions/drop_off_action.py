import math

from core.actions import Action
from core.buildings import Building
from core.units.villager import Villager


class DropOffAction(Action):

    def __init__(self, v: Villager, b: Building):
        self.set_involved_units(set([v]))
        self.building = b
        super().__init__()

    def do_action(self) -> bool:
        self.before_action()
        x, y = self.get_closest_tile_of_buiding_from_unit(
            (next(iter(self.get_involved_units())))
        )
        if (
            not math.sqrt(
                ((next(iter(self.get_involved_units()))).get_position().get_x() - x)
                ** 2
                + ((next(iter(self.get_involved_units()))).get_position().get_y() - y)
                ** 2
            )
            < 4
        ):
            return False

        self.building.drop_off_resources(next(iter(self.get_involved_units())))

        self.after_action()
        return True

    def get_closest_tile_of_buiding_from_unit(self, v: Villager):
        x = v.get_position().get_x()
        y = v.get_position().get_y()
        x_b = self.building.get_position().get_x()
        y_b = self.building.get_position().get_y()
        w = self.building.get_width()
        h = self.building.get_height()
        x = min(max(x, x_b), x_b + w)
        y = min(max(y, y_b), y_b + h)
        return x, y
