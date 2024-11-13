import pytest

from core.buildings import Building
from core.players import Player
from core.position import Position
from core.resource import Resource
@pytest.fixture
def my_house()->Building:
    my_pos = Position(45, 80)
    my_cost = Resource(135, 0, 0)
    my_player = Player("Philip", "red")
    return  Building(100, 4, 200, my_pos, 4, False, my_cost,my_player)

def test_correct_width_and_height():
    my_player = Player("Philip", "red")
    my_pos = Position(45, 80)
    my_cost = Resource(135, 0, 0)
    with pytest.raises(AssertionError):
        b = Building(100, 4, 200, my_pos, -4, False, my_cost,my_player)
    with pytest.raises(AssertionError):
        b= Building(100, -4, 200, my_pos, -4, False, my_cost,my_player)
    with pytest.raises(AssertionError):
        b = Building(100, -4, 200, my_pos, 4, False, my_cost,my_player)

def test_get_build_time(my_house: Building):
    assert my_house.get_build_time() == 100

def test_get_building_percent(my_house: Building) :
    assert my_house.get_building_percent() == 0

def test_get_height(my_house: Building):
    assert my_house.get_height() == 4

def test_get_health_point(my_house: Building):
    assert my_house.get_health_points() == 200

def test_get_width(my_house: Building):
    assert my_house.get_width() == 4

def test_get_position(my_house: Building):
    assert my_house.get_position().get_x() == 45
    assert my_house.get_position().get_y() == 80

def test_is_walkable(my_house: Building):
    assert my_house.is_walkable() == False

def test_is_built(my_house : Building):
    assert my_house.is_built()==False

def test_get_cost_resource(my_house: Building):
    assert my_house.get_cost_resource().get_wood() == 135
    assert my_house.get_cost_resource().get_food() == 0
    assert my_house.get_cost_resource().get_gold() == 0

def test_remove_health_point_gentle_hit(my_house: Building):  # the amount of health point removed is less than the total
    my_house.remove_health_points(57)
    assert my_house.get_health_points() == 143

def test_remove_health_point_overkill(my_house: Building):  # the amount of health point removed is more than the total
    my_house.remove_health_points(357)
    assert my_house.get_health_points() == -157

def test_remove_health_point_negative_hit(my_house: Building):  # verifying that it is impossible to hit a building for a negative damage value
    with pytest.raises(AssertionError):
        my_house.remove_health_points(-57)

def test_get_player(my_house : Building):
    assert my_house.get_player().get_name() == "Philip"
    assert my_house.get_player().get_color() == "red"






