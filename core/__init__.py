
from core.map import Map
from core.players import Player
from core.units import Unit
from core.buildings import Building

class Game:

    def __init__(self, players: set[Player], map: Map):
        if len(players) < 2:
            raise ValueError("A game must have at least two players.")
        self.__players = players
        self.__map = map

    def get_map(self) -> Map:
        return self.__map

    def get_players(self) -> set[Player]:
        return self.__players

    """
      def create_unit(self, type: str, building: Building) -> Unit:
          if type == "Villager":
              unit = Unit(player=building.get_player(), map=building.get_map(), position=building.get_position(), attack_speed=1.0, health_points=100, damage=10, movement_speed=1.0, range=1.0, training_time=1.0)
          else:
              raise ValueError(f"Unknown unit type: {type}")
          return unit
    """
