import math
from datetime import timedelta

from core.actions import Action
from core.buildings import Building
from core.units.villager import Villager


class BuildAction(Action):

    builders : set[Villager]
    building : Building
    nb_builders : int


    def __init__(self, b : Building):
        self.building = b
        self.builders = set()
        self.nb_builders =0
        super().__init__()


    def do_action(self)-> bool:
        self.before_action()
        if (self.get_new_time() - self.get_old_time()) > timedelta(seconds= 1):
            if self.nb_builders > 0 :
                self.building.build(100/(3*self.building.get_build_time()/(self.nb_builders+2)))
        self.after_action()
        return self.building.is_built()





    def add_builder(self, v : Villager):
        assert v.get_player() == self.building.get_player() , "builders must have same player as building"
        difx = v.get_position().get_x() - self.building.get_position().get_x()
        dify = v.get_position().get_y() - self.building.get_position().get_y()
        if math.sqrt(difx ** 2 + dify ** 2) < 4:
            self.builders.add(v)
            self.nb_builders +=1


