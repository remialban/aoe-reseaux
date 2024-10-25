

import pytest

from core.position import Position
from core.resources_points import ResourcePoint

from core.resource import Resource

p :Position = Position(15, 20)

@pytest.fixture
def stock_empty() -> Resource:
    return Resource(0,0,0)

@pytest.fixture
def stock_almost_full() -> Resource:
    return Resource(59,40,0)

@pytest.fixture
def stock_full() -> Resource:
    return Resource(50,50,0)

@pytest.fixture
def max_stock() -> int:
    return 100

@pytest.fixture
def resource_gold() -> Resource:
    return Resource(0,600,0)

@pytest.fixture
def resource_wood() -> Resource:
    return Resource(600,0,0)

@pytest.fixture
def rpgd(resource_gold) -> ResourcePoint:
    return ResourcePoint(p, resource_gold)

@pytest.fixture
def rpwd(resource_wood) -> ResourcePoint:
    return ResourcePoint(p, resource_wood)




#Pour un stock vide (gold):

def test_get_position_e(rpgd) :
    assert rpgd.get_position() == p

def test_collect_gold_with_resource_point_not_full(stock_empty, max_stock):
    rp=ResourcePoint(p, Resource(0,50,0))
    with pytest.raises(AssertionError):
        rp.collect(99,max_stock,stock_empty)

def test_wrong_resource_point_e(max_stock, stock_empty):
    bad_resource_point=ResourcePoint(p,Resource(600,900,500))
    assert bad_resource_point.collect(15,max_stock,stock_empty) == -1

def test_collect_gold_normal_e(rpgd : ResourcePoint, max_stock, stock_empty):
    rpgd.collect(15, max_stock,stock_empty)
    assert stock_empty.get_gold() == 15

def test_collect_gold_negative_e( max_stock, stock_empty, rpgd):
    with pytest.raises(AssertionError):
        rpgd.collect(-15,max_stock,stock_empty)
    assert stock_empty.get_gold() == 0

def test_collect_gold_null_e(rpgd : ResourcePoint, max_stock, stock_empty):
    with pytest.raises(AssertionError):
        rpgd.collect(0, max_stock,stock_empty)
    assert stock_empty.get_gold() == 0

def test_collect_gold_too_high_number_e(rpgd : ResourcePoint, stock_empty, max_stock):
    assert rpgd.collect(1000, max_stock , stock_empty) == 0
    assert stock_empty.get_gold() == 0


#pour un stock presque remplie (gold) :

def test_wrong_resource_point_alf(max_stock, stock_almost_full):
    bad_resource_point=ResourcePoint(p,Resource(600,900,500))
    assert bad_resource_point.collect(15,max_stock,stock_almost_full) == 0

def test_collect_gold_normal_alf(rpgd : ResourcePoint, max_stock, stock_almost_full):
    assert rpgd.collect(15, max_stock,stock_almost_full) == 0
    assert stock_almost_full.get_gold() == 40

def test_collect_gold_negative_alf( max_stock, stock_almost_full, rpgd):
    with pytest.raises(AssertionError):
        rpgd.collect(-15,max_stock,stock_almost_full)
    assert stock_almost_full.get_gold() == 40

def test_collect_gold_null_alf(rpgd : ResourcePoint, max_stock, stock_almost_full):
    with pytest.raises(AssertionError):
        rpgd.collect(0, max_stock,stock_almost_full)
    assert stock_almost_full.get_gold() == 40

def test_collect_gold_too_high_number_alf(rpgd : ResourcePoint, stock_almost_full, max_stock):
    assert rpgd.collect(1000, max_stock , stock_almost_full) == 0
    assert stock_almost_full.get_gold() == 40



#pour un stock remplie (gold) :

def test_wrong_resource_point_f(max_stock, stock_full):
    bad_resource_point=ResourcePoint(p,Resource(600,900,500))
    assert bad_resource_point.collect(15,max_stock,stock_full) == 0

def test_collect_gold_normal_f(rpgd : ResourcePoint, max_stock, stock_full):
    assert rpgd.collect(15, max_stock,stock_full) == 0
    assert stock_full.get_gold() == 50

def test_collect_gold_negative_f( max_stock, stock_full, rpgd):
    with pytest.raises(AssertionError):
        rpgd.collect(-15,max_stock,stock_full)
    assert stock_full.get_gold() == 50

def test_collect_gold_null_f(rpgd : ResourcePoint, max_stock, stock_full):
    assert rpgd.collect(0, max_stock,stock_full) == 0
    assert stock_full.get_gold() == 50

def test_collect_gold_too_high_number_f(rpgd : ResourcePoint, stock_full, max_stock):
    assert rpgd.collect(1000, max_stock , stock_full) == 0
    assert stock_full.get_gold() == 50




#Pour un stock vide (bois):

def test_collect_wood_with_resource_point_not_full(stock_empty, max_stock):
    rp=ResourcePoint(p, Resource(78,0,0))
    with pytest.raises(AssertionError):
        rp.collect(99,max_stock,stock_empty)

def test_collect_wood_normal_e(rpwd : ResourcePoint, max_stock, stock_empty):
    rpwd.collect(15, max_stock,stock_empty)
    assert stock_empty.get_wood() == 15

def test_collect_wood_negative_e_wood( max_stock, stock_empty, rpwd):
    with pytest.raises(AssertionError):
        rpwd.collect(-15,max_stock,stock_empty)
    assert stock_empty.get_wood() == 0

def test_collect_wood_null_e_wood(rpwd : ResourcePoint, max_stock, stock_empty):
    with pytest.raises(AssertionError):
        rpwd.collect(0, max_stock,stock_empty)
    assert stock_empty.get_wood() == 0

def test_collect_wood_too_high_number_e_wood(rpwd : ResourcePoint, stock_empty, max_stock):
    assert rpwd.collect(1000, max_stock , stock_empty) == 0
    assert stock_empty.get_wood() == 0


#pour un stock presque remplie (bois) :


def test_collect_wood_normal_alf_wood(rpwd : ResourcePoint, max_stock, stock_almost_full):
    assert rpwd.collect(15, max_stock,stock_almost_full) == 0
    assert stock_almost_full.get_wood() == 59

def test_collect_wood_negative_alf_wood( max_stock, stock_almost_full, rpwd):
    with pytest.raises(AssertionError):
        rpwd.collect(-15,max_stock,stock_almost_full)
    assert stock_almost_full.get_wood() == 59

def test_collect_wood_null_alf_wood(rpwd : ResourcePoint, max_stock, stock_almost_full):
    with pytest.raises(AssertionError):
        rpwd.collect(0, max_stock,stock_almost_full)
    assert stock_almost_full.get_wood() == 59

def test_collect_wood_too_high_number_alf_wood(rpwd : ResourcePoint, stock_almost_full, max_stock):
    assert rpwd.collect(1000, max_stock , stock_almost_full) == 0
    assert stock_almost_full.get_wood() == 59



#pour un stock remplie (bois) :

def test_collect_wood_normal_f_wood(rpwd : ResourcePoint, max_stock, stock_full):
    assert rpwd.collect(15, max_stock,stock_full) == 0
    assert stock_full.get_wood() == 50

def test_collect_wood_negative_f_wood( max_stock, stock_full, rpwd):
    with pytest.raises(AssertionError):
        rpwd.collect(-15,max_stock,stock_full)
    assert stock_full.get_gold() == 50

def test_collect_wood_null_f_wood(rpwd : ResourcePoint, max_stock, stock_full):
    assert rpwd.collect(0, max_stock,stock_full) == 0
    assert stock_full.get_wood() == 50

def test_collect_wood_too_high_number_f_wood(rpwd : ResourcePoint, stock_full, max_stock):
    assert rpwd.collect(1000, max_stock , stock_full) == 0
    assert stock_full.get_wood() == 50

