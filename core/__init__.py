from core.actions import Action
from core.map import Map
from core.players import Player
from core.players.ai import AI
from core.units import Unit
from core.buildings import Building

class Game:

    __actions : set[Action]

    def __init__(self, players: set[Player], map: Map):
        if len(players) < 2:
            raise ValueError("A game must have at least two players.")
        self.__players = players
        self.__map = map
        self.__actions = set()

    def get_map(self) -> Map:
        return self.__map

    def get_players(self) -> set[Player]:
        return self.__players

    def add_action(self,action : Action):
        self.__actions.add(action)

    def remove_action(self, action : Action):
        self.__actions.remove(action)

    """
      def create_unit(self, type: str, building: Building) -> Unit:
          if type == "Villager":
              unit = Unit(player=building.get_player(), map=building.get_map(), position=building.get_position(), attack_speed=1.0, health_points=100, damage=10, movement_speed=1.0, range=1.0, training_time=1.0)
          else:
              raise ValueError(f"Unknown unit type: {type}")
          return unit
    """
    def party(self):

        while True:
            finished_actions : set[Action]= set()

            for p in self.__players :
                if isinstance(p,AI):
                    p.play()
            for a in self.__actions :
                if a.do_action():
                    finished_actions.add(a)

            for fa in finished_actions :
                self.__actions.remove(fa)








