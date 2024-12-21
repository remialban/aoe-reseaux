import pytest

from core import Map, Player
from core.actions.collect_action import Collect_Action
from core.buildings.farm import Farm
from core.position import Position
from core.resources_points.wood import Wood
from core.resources_points.mine import Mine
from core.units.villager import Villager

#normal case 4 error

p :Position = Position(15, 20)

@pytest.fixture
def villager():
    return Villager(Player("a","bleu"),Map(10,10),p,15,10,10,10,10,10,100)

@pytest.fixture
def mine() -> Mine:
    return Mine(p)

@pytest.fixture
def forest() -> Wood:
    return Wood(p)

@pytest.fixture
def wood(villager, forest) -> Collect_Action:
    return Collect_Action(villager,forest)

@pytest.fixture
def gold(villager, mine) -> Collect_Action:
    return Collect_Action(villager,mine)

#WOOD collect test

def test_do_action_collect_wood(wood):
    assert wood.do_action_collect() == 5
    assert wood.get_resource().get_wood() ==10

def test_do_action_collect_wood_in_range_3( wood):
    c=0
    for i in range(3):
        assert wood.do_action_collect() == 5
        assert wood.get_resource().get_wood() ==10 + c
        c=c + 10
    assert wood.get_resource().get_wood() == 30

def test_do_action_collect_wood_error( wood):
    assert wood.do_action_collect() == 5
    assert wood.get_resource().get_wood() == 20


#Gold collect test

def test_do_action_collect_gold( gold) :
    assert gold.do_action_collect() == 7
    assert gold.get_resource().get_gold() == 10

def test_do_action_collect_gold_error(gold) :
    assert gold.do_action_collect() == 7
    assert gold.get_resource().get_gold() == 20

def test_do_action_collect_gold_in_range_3( gold):
    c=0
    for i in range(3):
        assert gold.do_action_collect() == 7
        assert gold.get_resource().get_gold() ==10 + c
        c=c + 10
    assert gold.get_resource().get_gold() == 30

#Villager collect inventory test for wood

def test_villager_wood(wood,villager):
    assert wood.do_action_collect() == 5
    assert wood.get_resource().get_wood() == 10
    assert villager.get_stock()["wood"] == 10

def test_villager_wood_in_range_3(wood,villager):
    c = 0
    for i in range(3):
        assert wood.do_action_collect() == 5
        assert wood.get_resource().get_wood() == 10 + c
        assert villager.get_stock()["wood"] == 10 + c
        c = c + 10
    assert villager.get_stock()["wood"] == 30
    assert wood.get_resource().get_wood() == 30

def test_villager_wood_in_range_8(wood,villager):
    c = 0
    for i in range(8):
        assert wood.do_action_collect() == 5
        assert wood.get_resource().get_wood() == 10 + c
        assert villager.get_stock()["wood"] == 10 + c
        c = c + 10
    assert villager.get_stock()["wood"] == 80
    assert wood.get_resource().get_wood() == 80

def test_villager_wood_in_range_11(wood, villager):
        c = 0
        for i in range(11):
            assert wood.do_action_collect() == 5
            assert wood.get_resource().get_wood() == 10 + c
            assert villager.get_stock()["wood"] == 10 + c
            if c<90:c = c + 10
            else: break
        assert villager.get_stock()["wood"] == 100
        assert wood.get_resource().get_wood() == 100


def test_villager_wood_in_range_11_error(wood, villager):
        c = 0
        for i in range(11):
            assert wood.do_action_collect() == 5
            assert wood.get_resource().get_wood() == 10 + c
            assert villager.get_stock()["wood"] == 10 + c
            c = c + 10
        assert villager.get_stock()["wood"] == 110
        assert wood.get_resource().get_wood() == 110

#Villager collect inventory test for gold

def test_villager_gold(gold,villager):
    assert gold.do_action_collect() == 7
    assert gold.get_resource().get_gold() == 10
    assert villager.get_stock()["gold"] == 10

def test_villager_gold_in_range_3( gold,villager):
    c=0
    for i in range(3):
        assert gold.do_action_collect() == 7
        assert gold.get_resource().get_gold() ==10 + c
        assert villager.get_stock()["gold"] == 10 +c
        c=c + 10
    assert villager.get_stock()["gold"] == 30
    assert gold.get_resource().get_gold() == 30

def test_villager_gold_in_range_8( gold,villager):
    c=0
    for i in range(8):
        assert gold.do_action_collect() == 7
        assert gold.get_resource().get_gold() ==10 + c
        assert villager.get_stock()["gold"] == 10 +c
        c=c + 10
    assert villager.get_stock()["gold"] == 80
    assert gold.get_resource().get_gold() == 80

def test_villager_gold_in_range_11( gold,villager):
    c=0
    for i in range(11):
        assert gold.do_action_collect() == 7
        assert gold.get_resource().get_gold() ==10 + c
        assert villager.get_stock()["gold"] == 10 +c
        if c<90:c=c + 10
        else: break
    assert villager.get_stock()["gold"] == 100
    assert gold.get_resource().get_gold() == 100


def test_villager_gold_in_range_11_error( gold,villager):
    c=0
    for i in range(11):
        assert gold.do_action_collect() == 7
        assert gold.get_resource().get_gold() ==10 + c
        assert villager.get_stock()["gold"] == 10 +c
        c=c + 10
    assert villager.get_stock()["gold"] == 110
    assert gold.get_resource().get_gold() == 110