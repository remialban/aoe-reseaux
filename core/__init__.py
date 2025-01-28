from core.actions import Action
from core.map import Map
from core.players import Player
from core.players.ai import AI
from core.buildings.town_center import TownCenter
from core.buildings.stable import Stable
from core.buildings.barracks import Barracks
from core.buildings.archery_range import ArcheryRange
from core.buildings import Building


class Game:

    __actions: set[Action]
    __paused: bool

    def __init__(self, players: set[Player], map: Map):
        # if len(players) < 2:
        #     raise ValueError("A game must have at least two players.")
        self.__players = players
        self.__map = map
        self.__actions = set()
        self.__paused = False

    def get_map(self) -> Map:
        return self.__map

    def get_players(self) -> set[Player]:
        return self.__players

    def add_action(self, action: Action):
        self.__actions.add(action)

    def remove_action(self, action: Action):
        self.__actions.remove(action)

    def pause(self):
        self.__paused = True
        for a in self.__actions:
            a.save_time_delta()

    def get_actions(self) -> set[Action]:
        return self.__actions

    def resume(self):
        for a in self.__actions:
            a.before_action()
            a.set_old_time(a.get_new_time() - a.get_saved_time_delta())
        self.__paused = False

    """
      def create_unit(self, type: str, building: Building) -> Unit:
          if type == "Villager":
              unit = Unit(player=building.get_player(), map=building.get_map(), position=building.get_position(), attack_speed=1.0, health_points=100, damage=10, movement_speed=1.0, range=1.0, training_time=1.0)
          else:
              raise ValueError(f"Unknown unit type: {type}")
          return unit
    """

    def party(self):
        if not self.__paused:
            finished_actions: set[Action] = set()
            # print("Players:", self.__players)
            for p in self.__players:
                # print("Isinstance AI?", isinstance(p, AI))
                if isinstance(p, AI):
                    # print("Playing AI for player", p.get_name())
                    p.play(self)
            print("====================== ACTIONS ======================")
            for a in self.__actions:
                print(type(a).__name__)
                if a.do_action():
                    # print("Action finished")
                    finished_actions.add(a)
            print("=====================================================")

            for fa in finished_actions:
                self.__actions.remove(fa)

            self.__map.clean()

            victory = self.check_victory()

            if victory:
                exit(f"Player {victory.get_name()} has won the game!")

        self.__map.clean()

        # input("Press Enter to continue...")

    def is_paused(self):
        return self.__paused

    def check_victory(self):
        defeated_players = []
        for player in self.__players:
            if (
                # not self.__map.get_units(player)
                self.__map.get_units(player)
                and (
                    not any(
                        isinstance(building, TownCenter)
                        for building in self.__map.get_buildings(player)
                    )
                    and not any(
                        isinstance(building, Stable)
                        for building in self.__map.get_buildings(player)
                    )
                    and not any(
                        isinstance(building, Barracks)
                        for building in self.__map.get_buildings(player)
                    )
                    and not any(
                        isinstance(building, ArcheryRange)
                        for building in self.__map.get_buildings(player)
                    )
                )
                or (
                    # not self.__map.get_units(player)
                    self.__map.get_units(player)
                    and (
                        player.get_stock().get_wood() == 0
                        and player.get_stock().get_gold() == 0
                        and player.get_stock().get_food() == 0
                    )
                )
            ):
                defeated_players.append(player)

        if len(defeated_players) == len(self.__players) - 1:
            for player in self.__players:
                if player not in defeated_players:
                    return player
        return None
