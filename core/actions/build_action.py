import math
from datetime import timedelta

from core.actions import Action
from core.buildings import Building
from core.units.villager import Villager


class BuildAction(Action):

    builders: set[Villager]
    building: Building
    nb_builders: int

    def __init__(self, b: Building):
        self.building = b
        self.set_involved_units(set())
        self.nb_builders = 0
        super().__init__()

    def do_action(self) -> bool:
        self.before_action()
        # difx = v.get_position().get_x() - self.building.get_position().get_x()
        # dify = v.get_position().get_y() - self.building.get_position().get_y()
        # assert not math.sqrt(difx**2 + dify**2) < 4, "builder too far"

        # check all builders are math.sqrt(difx**2 + dify**2) < 4 from the building (using width and height of building)
        if [v for v in self.get_involved_units() if v.get_health_points() <= 0]:
            self.building.remove_health_points(self.building.get_health_points())
            return True
        for v in self.get_involved_units():
            x, y = self.get_closest_tile_of_buiding_from_unit(v)
            # print(f"builder at {v.get_position().get_x()} {v.get_position().get_y()} closest tile {x} {y}")
            # print(f"distance {math.sqrt((v.get_position().get_x() - x)**2 + (v.get_position().get_y() - y)**2)}")
            if (
                not math.sqrt(
                    (v.get_position().get_x() - x) ** 2
                    + (v.get_position().get_y() - y) ** 2
                )
                < 4
            ):
                return False
        # print("all builders are close enough")
        if (self.get_new_time() - self.get_old_time()) > timedelta(seconds=1):
            if self.nb_builders > 0:
                self.building.build(
                    100
                    / (
                        3 * self.building.get_build_time() / (self.nb_builders + 2)
                    )  # * 20 # SPEED
                )
            self.after_action()
            return self.building.is_built()
        return False

    def add_builder(self, v: Villager):
        assert (
            v.get_player() == self.building.get_player()
        ), "builders must have same player as building"
        assert not v in self.get_involved_units(), "builder already added"
        assert not self.building.is_built(), "building already built"
        assert self.nb_builders <= 3, "too many builders"
        # v.set_busy(True)
        self.set_involved_units(self.get_involved_units().union(set([v])))
        self.nb_builders += 1

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

    def get_list_attributes(self):
        return [[self.building.id, "building_percent"]]
