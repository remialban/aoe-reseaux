from datetime import timedelta

import pytest

from core.actions.attack_building_action import AttackBuildingAction
from core.actions.attack_unit_action import AttackUnitAction
from core.actions.attack_unit_by_building_action import AttackUnitByBuildingAction
from core.buildings import Building
from core.buildings.keep import Keep
from core.map import Map
from core.players import Player
from core.position import Position
from core.resource import Resource
from core.units import Unit


@pytest.fixture
def my_attack_building_action()->AttackBuildingAction:
    my_map= Map(120,120)
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    my_cost = Resource(135, 0, 0)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza","blue")
    my_house = Building(100, 4, 200, my_pos, 4, False, my_cost,my_player)
    my_unit = Unit(my_other_player,my_map,my_other_pos,2,100,20,1.2,3,15)
    return AttackBuildingAction(my_unit, my_house)

@pytest.fixture
def my_attack_unit_action()->AttackUnitAction:
    my_map= Map(120,120)
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza","blue")
    my_other_unit = Unit(my_player, my_map, my_pos, 2, 100, 20, 11.2,3,15)
    my_unit = Unit(my_other_player,my_map,my_other_pos,2,100,20,1.2,3,15)
    return AttackUnitAction(my_unit,my_other_unit )

@pytest.fixture
def my_attack_unit_by_building_action()->AttackUnitByBuildingAction:
    my_map= Map(120,120)
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza","blue")
    my_other_unit = Unit(my_player, my_map, my_pos, 2, 100, 20, 11.2,3,15)
    my_keep = Keep(my_other_pos, my_other_player)
    return AttackUnitByBuildingAction(my_keep,my_other_unit )


def test_initialisation_attack_building(my_attack_building_action) :
    assert (my_attack_building_action.get_new_time() - my_attack_building_action.get_old_time() ) >= timedelta(seconds = 80)

def test_before_and_after_action_attack_building(my_attack_building_action) :
    my_attack_building_action.before_action()
    my_attack_building_action.after_action()
    assert (my_attack_building_action.get_new_time() - my_attack_building_action.get_old_time() ) < timedelta(seconds = 2)

def test_do_action_attack_building_sufficient_range() :
    my_map= Map(120,120)
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    my_cost = Resource(135, 0, 0)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza","blue")
    my_house = Building(100, 4, 200, my_pos, 4, False, my_cost,my_player)
    my_unit = Unit(my_other_player,my_map,my_other_pos,2,100,20,1.2,3,15)
    aba = AttackBuildingAction(my_unit, my_house)
    aba.do_action()
    assert my_house.get_health_points() == 180

def test_do_action_attack_building_insufficient_range() :
    my_map= Map(120,120)
    my_pos = Position(45, 80)
    my_other_pos = Position(55, 80)
    my_cost = Resource(135, 0, 0)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza","blue")
    my_house = Building(100, 4, 200, my_pos, 4, False, my_cost,my_player)
    my_unit = Unit(my_other_player,my_map,my_other_pos,2,100,20,1.2,3,15)
    aba = AttackBuildingAction(my_unit, my_house)
    aba.do_action()
    assert my_house.get_health_points() == 200



def test_initialisation_attack_unit(my_attack_unit_action) :
    assert (my_attack_unit_action.get_new_time() - my_attack_unit_action.get_old_time() ) >= timedelta(seconds = 80)

def test_before_and_after_action_attack_unit(my_attack_unit_action) :
    my_attack_unit_action.before_action()
    my_attack_unit_action.after_action()
    assert (my_attack_unit_action.get_new_time() - my_attack_unit_action.get_old_time() ) < timedelta(seconds = 2)


def test_do_action_attack_unit_sufficient_range():
    my_map = Map(120, 120)
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza", "blue")
    my_other_unit = Unit(my_player, my_map, my_pos, 2, 100, 20, 11.2, 3, 15)
    my_unit = Unit(my_other_player, my_map, my_other_pos, 2, 100, 20, 1.2, 3, 15)
    aua = AttackUnitAction(my_unit, my_other_unit)
    aua.do_action()
    assert my_other_unit.get_health_points() == 80

def test_do_action_attack_unit_insufficient_range():
    my_map = Map(120, 120)
    my_pos = Position(45, 80)
    my_other_pos = Position(55, 80)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza", "blue")
    my_other_unit = Unit(my_player, my_map, my_pos, 2, 100, 20, 11.2, 3, 15)
    my_unit = Unit(my_other_player, my_map, my_other_pos, 2, 100, 20, 1.2, 3, 15)
    aua = AttackUnitAction(my_unit, my_other_unit)
    aua.do_action()
    assert my_other_unit.get_health_points() == 100


def test_initialisation_attack_unit_by_building(my_attack_unit_by_building_action) :
    assert (my_attack_unit_by_building_action.get_new_time() - my_attack_unit_by_building_action.get_old_time() ) >= timedelta(seconds = 80)

def test_before_and_after_action_attack_unit_by_building(my_attack_unit_by_building_action) :
    my_attack_unit_by_building_action.before_action()
    my_attack_unit_by_building_action.after_action()
    assert (my_attack_unit_by_building_action.get_new_time() - my_attack_unit_by_building_action.get_old_time() ) < timedelta(seconds = 2)

def test_do_action_attack_unit_by_building_sufficient_range():
    my_map= Map(120,120)
    my_pos = Position(45, 80)
    my_other_pos = Position(47, 80)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza","blue")
    my_other_unit = Unit(my_player, my_map, my_pos, 2, 100, 20, 11.2,3,15)
    my_keep = Keep(my_other_pos, my_other_player)
    aubba = AttackUnitByBuildingAction(my_keep, my_other_unit)
    aubba.do_action()
    assert my_other_unit.get_health_points() == 96

def test_do_action_attack_unit_insufficient_range():
    my_map= Map(120,120)
    my_pos = Position(45, 80)
    my_other_pos = Position(55, 80)
    my_player = Player("Leopold", "red")
    my_other_player = Player("Querza","blue")
    my_other_unit = Unit(my_player, my_map, my_pos, 2, 100, 20, 11.2,3,15)
    my_keep = Keep(my_other_pos, my_other_player)
    aubba = AttackUnitByBuildingAction(my_keep, my_other_unit)
    aubba.do_action()
    assert my_other_unit.get_health_points() == 100

