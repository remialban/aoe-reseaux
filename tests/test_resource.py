import pytest

from core.resource import Resource


def test_constructor(resource: Resource):
    assert resource.get_food() == 45
    assert resource.get_gold() == 23
    assert resource.get_wood() == 10

@pytest.fixture
def resource() -> Resource:
    return Resource(10,23,45)

def test_remove_food_too_high_number(resource: Resource):
    with pytest.raises(AssertionError):
        resource.remove_food(90)
    assert resource.get_food() == 45

def test_remove_gold_too_high_number(resource: Resource):
    with pytest.raises(AssertionError):
        resource.remove_gold(90)
    assert resource.get_gold() == 23

def test_remove_wood_too_high_number(resource : Resource):
    with pytest.raises(AssertionError):
        resource.remove_wood(90)
    assert resource.get_wood() == 10

def test_remove_food_normal_case(resource: Resource):
    resource.remove_food(44)
    assert resource.get_food() == 1

def test_remove_gold_normal_case(resource: Resource):
    resource.remove_gold(22)
    assert resource.get_gold() == 1

def test_remove_wood_normal_case(resource : Resource):
    resource.remove_wood(9)
    assert resource.get_wood() == 1

def test_remove_food_negative(resource: Resource):
    with pytest.raises(AssertionError):
        resource.remove_food(-44)
    assert resource.get_food() == 45

def test_remove_gold_negative(resource: Resource):
    with pytest.raises(AssertionError):
        resource.remove_gold(-22)
    assert resource.get_gold() == 23

def test_remove_wood_negative(resource : Resource):
    with pytest.raises(AssertionError):
        resource.remove_wood(-9)
    assert resource.get_wood() == 10

def test_remove_food_null(resource: Resource):
    resource.remove_food(0)
    assert resource.get_food() == 45

def test_remove_gold_null(resource: Resource):
    resource.remove_gold(0)
    assert resource.get_gold() == 23

def test_remove_wood_null(resource : Resource):
    resource.remove_wood(0)
    assert resource.get_wood() == 10




def test_add_food(resource: Resource):
    resource.add_food(90)
    assert resource.get_food() == 135

def test_add_gold(resource: Resource):
    resource.add_gold(90)
    assert resource.get_gold() == 113

def test_add_wood(resource : Resource):
    resource.add_wood(90)
    assert resource.get_wood() == 100

def test_add_food_null(resource: Resource):
    resource.add_food(0)
    assert resource.get_food() == 45

def test_add_gold_null(resource: Resource):
    resource.add_gold(0)
    assert resource.get_gold() == 23

def test_add_wood_null(resource : Resource):
    resource.add_wood(0)
    assert resource.get_wood() == 10

def test_add_food_negative(resource: Resource):
    with pytest.raises(AssertionError):
        resource.add_food(-90)
    assert resource.get_food() == 45

def test_add_gold_negative(resource: Resource):
    with pytest.raises(AssertionError):
        resource.add_gold(-90)
    assert resource.get_gold() == 23

def test_add_wood_negative(resource : Resource):
    with pytest.raises(AssertionError):
        resource.add_wood(-90)
    assert resource.get_wood() == 10


def test_constructor_negative_value():
    with pytest.raises(AssertionError):
        Resource(-5,-5,-5)