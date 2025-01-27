
import pytest

from core.actions.build_action import BuildAction
from core.buildings.keep import Keep
from core.map import Map, Modes
from core.players import Player
from core.position import Position
from core.units.villager import Villager

d = 0.00001
@pytest.fixture
def my_build_action()->BuildAction:
    my_player = Player("Leopold", "red")
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    v1 = Villager(my_player,my_pos)
    my_building = Keep(my_other_pos,my_player)
    my_build_action = BuildAction(my_building)
    my_build_action.add_builder(v1)
    return my_build_action


def test_build_progression_1_villager(my_build_action):
    a = my_build_action.building.get_building_percent()
    my_build_action.do_action()
    assert d > abs(my_build_action.building.get_building_percent() - a - (100/my_build_action.building.get_build_time()))

def test_build_progression_2_villagers():
    my_player = Player("Leopold", "red")
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    any_other_pos = Position(47,83)
    v1 = Villager(my_player,my_pos)
    v2 = Villager(my_player,any_other_pos)
    my_building = Keep(my_other_pos,my_player)
    my_build_action = BuildAction(my_building)
    my_build_action.add_builder(v1)
    my_build_action.add_builder(v2)
    a = my_build_action.building.get_building_percent()
    my_build_action.do_action()
    assert d > abs(my_build_action.building.get_building_percent() - a - (100*4/my_build_action.building.get_build_time()/3))

def test_add_build_different_player(my_build_action):
    any_other_pos = Position(47,83)
    irvin = Player("Irvin","blue")
    v2 = Villager(irvin,any_other_pos)
    with pytest.raises(AssertionError):
        my_build_action.add_builder(v2)

