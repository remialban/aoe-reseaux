from core.actions.move_action import MoveAction
from core.map import Map
from core.players import Player
from core.position import Position
from core.units import Unit
from core.buildings import Building
from core.resource import Resource
from core.buildings.keep import Keep
from core.buildings.farm import Farm
import time


def test_do_action_move_unit():
    my_map = Map(5, 2)
    # Create a map with a unit, a farm and a keep
    # Lets put the unit at (0, 0), the farm at (1, 0) and the keep at (2, 0) and we need to move the unit to (3,0)
    player = Player("player1", "blue")
    unit = Unit(player, my_map, Position(0, 0), 2, 100, 20, 1.2, 3, 15)
    farm = Farm(Position(1, 0), player)
    keep = Keep(Position(2, 0), player)
    my_map.add_unit(unit)
    my_map.add_building(farm)
    my_map.add_building(keep)

	# Create a move action
    action = MoveAction(my_map, unit, Position(3, 0))
    # Perform the action
    start_time = time.time()
    while not action.do_action():
        time.sleep(0.01)
    end_time = time.time()
    print(f"Time taken to move unit: {end_time - start_time}")
    # Check if the unit is at the right position
    assert unit.get_position() == Position(3, 0)