import pytest


from core import Game, AI, Map, Player
from core.actions.attack_building_action import AttackBuildingAction
from core.actions.attack_unit_action import AttackUnitAction
from core.actions.build_action import BuildAction
from core.buildings.archery_range import ArcheryRange
from core.map import Modes
from core.position import Position
from core.units.villager import Villager


@pytest.fixture
def tgame():
    phil = AI("Philip","red")
    phili = AI("Philipine","blue")
    philworld = Map(124,124)
    philipains = set()
    philipains.add(phil)
    philipains.add(phili)
    tgame = Game(philipains,philworld)
    return tgame


def test_game_loop(tgame):
    pos1 = Position(33,33)
    phil = AI("phil","red")
    oswald = Villager(phil, pos1)
    pos2 = Position(33,34)
    phol = AI("phol","red")
    baldur = Villager(phol,pos2)
    a1 = AttackUnitAction(oswald,baldur)
    a2 = AttackUnitAction(oswald, baldur)
    a3 = AttackUnitAction(oswald, baldur)
    a4 = AttackUnitAction(oswald, baldur)

    tgame.add_action(a1)
    tgame.add_action(a2)
    tgame.add_action(a3)
    tgame.add_action(a4)
    tgame.party()
    assert baldur.get_health_points() == 17




def test_pause_unpause() :
    phil = AI("Philip","red")
    phili = AI("Philipine","blue")
    m = Modes(3)
    philipains = set()
    philipains.add(phil)
    philipains.add(phili)
    philworld = Map(124,124,m,philipains)
    tgame = Game(philipains, philworld)
    pos = Position(52,84)
    other_pos = Position(53,84)
    v1 = Villager(phil,pos)
    arch = ArcheryRange(other_pos,phil)
    tgame.add_action(AttackBuildingAction(v1,arch))
    health = arch.get_health_points()
    tgame.pause()
    tgame.party()
    assert health == arch.get_health_points()
    tgame.resume()
    tgame.party()
    assert health > arch.get_health_points()








