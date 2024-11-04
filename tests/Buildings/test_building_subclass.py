import pytest

from core.buildings.archery_range import ArcheryRange
from core.buildings.barracks import Barracks
from core.buildings.camp import Camp
from core.buildings.farm import Farm
from core.buildings.house import House
from core.buildings.keep import Keep
from core.buildings.stable import Stable
from core.buildings.town_center import TownCenter
from core.position import Position



def test_farm_creation():
    p = Position(5, 6)
    f = Farm(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 2
    assert f.get_health_point() == 100
    assert f.get_build_time() == 10
    assert f.get_cost_resource().get_food() == f.get_cost_resource().get_gold() == 0
    assert f.get_cost_resource().get_wood() == 60
    assert f.is_walkable() == True
    assert f.resources.get_food() == 300
    assert f.resources.get_wood() == f.resources.get_gold() == 0
    f.collect(150)
    assert f.resources.get_food() == 150, "invalid resource collect"
    f.collect(300)
    assert f.resources.get_food() == 0,"negative resource"

def test_archery_range_creation():
    p = Position(5, 6)
    f = ArcheryRange(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 3
    assert f.get_health_point() == 500
    assert f.get_build_time() == 50
    assert f.get_cost_resource().get_food() == f.get_cost_resource().get_gold() == 0
    assert f.get_cost_resource().get_wood() == 175
    assert f.is_walkable() == False


def test_barrack_creation():
    p = Position(5, 6)
    f = Barracks(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 3
    assert f.get_health_point() == 500
    assert f.get_build_time() == 50
    assert f.get_cost_resource().get_food() == f.get_cost_resource().get_gold() == 0
    assert f.get_cost_resource().get_wood() == 175
    assert f.is_walkable() == False

def test_stable_creation():
    p = Position(5, 6)
    f = Stable(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 3
    assert f.get_health_point() == 500
    assert f.get_build_time() == 50
    assert f.get_cost_resource().get_food() == f.get_cost_resource().get_gold() == 0
    assert f.get_cost_resource().get_wood() == 175
    assert f.is_walkable() == False

def test_camp_creation():
    p = Position(5, 6)
    f = Camp(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 2
    assert f.get_health_point() == 200
    assert f.get_build_time() == 25
    assert f.get_cost_resource().get_food() == f.get_cost_resource().get_gold() == 0
    assert f.get_cost_resource().get_wood() == 100
    assert f.is_walkable() == False

def test_house_creation():
    p = Position(5, 6)
    f = House(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 2
    assert f.get_health_point() == 200
    assert f.get_build_time() == 25
    assert f.get_cost_resource().get_food() == f.get_cost_resource().get_gold() == 0
    assert f.get_cost_resource().get_wood() == 25
    assert f.is_walkable() == False

def test_town_center_creation():
    p = Position(5, 6)
    f = TownCenter(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 4
    assert f.get_health_point() == 1000
    assert f.get_build_time() == 150
    assert f.get_cost_resource().get_food() == f.get_cost_resource().get_gold() == 0
    assert f.get_cost_resource().get_wood() == 350
    assert f.is_walkable() == False

def test_keep_creation():
    p = Position(5, 6)
    f = Keep(p)
    assert f.get_position().get_x() == p.get_x()
    assert f.get_position().get_y() == p.get_y()
    assert f.get_width() == f.get_height() == 1
    assert f.get_health_point() == 800
    assert f.get_build_time() == 80
    assert f.get_cost_resource().get_food() == 0
    assert f.get_cost_resource().get_gold() == 125
    assert f.get_cost_resource().get_wood() == 35
    assert f.is_walkable() == False





