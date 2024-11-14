import pytest

from core.position import Position

from core.resources_points.wood import Wood

from core.resources_points.mine import Mine

from core.resource import Resource

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

p :Position = Position(15, 20)

@pytest.fixture
def w() -> Wood:
    return Wood(p)

@pytest.fixture
def m() -> Mine:
    return Mine(p)

def test_get_position_wood(w) :
    assert w.get_position() == p

def test_get_position_mine(m) :
    assert m.get_position() == p


#Pour un stock vide (gold):

def test_collect_gold_normal_e_mine(max_stock, stock_empty, m):
    m.collect(90, max_stock,stock_empty)
    assert stock_empty.get_gold() == 90

def test_collect_gold_negative_mine(max_stock, stock_empty, m):
    with pytest.raises(AssertionError):
        m.collect(-15,max_stock,stock_empty)
    assert stock_empty.get_gold() == 0

def test_collect_gold_null_mine(max_stock, stock_empty, m):
    with pytest.raises(AssertionError):
        m.collect(0, max_stock,stock_empty)
    assert stock_empty.get_gold() == 0

def test_collect_gold_too_high_number_mine( stock_empty, max_stock, m):
    assert m.collect(601, max_stock , stock_empty) == 0
    assert stock_empty.get_gold() == 0

#pour un stock presque rempli (gold) :


def test_collect_gold_normal_alf_mine(max_stock, stock_almost_full, m):
    assert m.collect(15, max_stock,stock_almost_full) == 0
    assert stock_almost_full.get_gold() == 40


def test_collect_gold_negative_alf_mine(max_stock, stock_almost_full, m):
    with pytest.raises(AssertionError):
        m.collect(-15,max_stock,stock_almost_full)
    assert stock_almost_full.get_gold() == 40

def test_collect_gold_null_alf_mine(max_stock, stock_almost_full, m):
    with pytest.raises(AssertionError):
        m.collect(0, max_stock,stock_almost_full)
    assert stock_almost_full.get_gold() == 40


def test_collect_gold_too_high_number_alf_mine(stock_almost_full, max_stock, m):
    assert m.collect(601, max_stock , stock_almost_full) == 0
    assert stock_almost_full.get_gold() == 40



#Pour un stock rempli (gold) :


def test_collect_gold_normal_f_mine(max_stock, stock_full, m):
    assert m.collect(15, max_stock,stock_full) == 0
    assert stock_full.get_gold() == 50

def test_collect_gold_negative_f_mine(max_stock, stock_full, m):
    with pytest.raises(AssertionError):
        m.collect(-15,max_stock,stock_full)
    assert stock_full.get_gold() == 50

def test_collect_gold_null_f_mine(max_stock, stock_full, m):
    assert m.collect(0, max_stock,stock_full) == 0
    assert stock_full.get_gold() == 50

def test_collect_gold_too_high_number_f_mine(stock_full, max_stock, m):
    assert m.collect(601, max_stock , stock_full) == 0
    assert stock_full.get_gold() == 50



#Pour un stock vide (bois):


def test_collect_wood_normal_e_wood(w, max_stock, stock_empty):
    w.collect(15, max_stock,stock_empty)
    assert stock_empty.get_wood() == 15

def test_collect_wood_negative_e_wood( max_stock, stock_empty, w):
    with pytest.raises(AssertionError):
        w.collect(-15,max_stock,stock_empty)
    assert stock_empty.get_wood() == 0

def test_collect_wood_null_e_wood(w, max_stock, stock_empty):
    with pytest.raises(AssertionError):
        w.collect(0, max_stock,stock_empty)
    assert stock_empty.get_wood() == 0

def test_collect_wood_too_high_number_e_wood(w, stock_empty, max_stock):
    assert w.collect(101, max_stock , stock_empty) == 0
    assert stock_empty.get_wood() == 0


#Pour un stock presque rempli (bois) :


def test_collect_wood_normal_alf_wood(w, max_stock, stock_almost_full):
    assert w.collect(15, max_stock,stock_almost_full) == 0
    assert stock_almost_full.get_wood() == 59

def test_collect_wood_negative_alf_wood( max_stock, stock_almost_full, w):
    with pytest.raises(AssertionError):
        w.collect(-15,max_stock,stock_almost_full)
    assert stock_almost_full.get_wood() == 59

def test_collect_wood_null_alf_wood(w, max_stock, stock_almost_full):
    with pytest.raises(AssertionError):
        w.collect(0, max_stock,stock_almost_full)
    assert stock_almost_full.get_wood() == 59

def test_collect_wood_too_high_number_alf_wood(w, stock_almost_full, max_stock):
    assert w.collect(101, max_stock , stock_almost_full) == 0
    assert stock_almost_full.get_wood() == 59



#Pour un stock rempli (bois) :

def test_collect_wood_normal_f_wood(w, max_stock, stock_full):
    assert w.collect(15, max_stock,stock_full) == 0
    assert stock_full.get_wood() == 50

def test_collect_wood_negative_f_wood( max_stock, stock_full, w):
    with pytest.raises(AssertionError):
        w.collect(-15,max_stock,stock_full)
    assert stock_full.get_gold() == 50

def test_collect_wood_null_f_wood(w, max_stock, stock_full):
    assert w.collect(0, max_stock,stock_full) == 0
    assert stock_full.get_wood() == 50

def test_collect_wood_too_high_number_f_wood(w, stock_full, max_stock):
    assert w.collect(1000, max_stock , stock_full) == 0
    assert stock_full.get_wood() == 50


