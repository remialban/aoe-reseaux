import pytest

from core.position import Position


@pytest.fixture
def position():
    return Position(10.58, 20.12)


def test_position_init(position: Position):
    assert position.get_x() == pytest.approx(10.58, abs=0.02)
    assert position.get_y() == pytest.approx(20.12, abs=0.02)


def test_position_setter(position: Position):
    position.set_x(50.5)
    position.set_y(90.2)

    assert position.get_x() == pytest.approx(50.5, abs=0.02)
    assert position.get_y() == pytest.approx(90.2, abs=0.02)
