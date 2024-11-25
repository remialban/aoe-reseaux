import pytest


from core import Game, AI, Map, Player


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
    tgame.party()




