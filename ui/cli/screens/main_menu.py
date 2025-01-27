import unicurses as curses

from core import Player, Map, Game
from core.actions.move_action import MoveAction
from core.map import RessourceModes, PlayerModes
from core.units.archer import Archer
from core.units.horse_man import Horseman
from core.units.villager import Villager
from ui.cli import Screen, GameMenu, ScreenManager, Screens
from ui.enums import UIList
from ui.ui_manager import UIManager
from core.position import Position

class MainMenu(Screen):
    def __init__(self, window):
        super().__init__(window)
        self.__choices = ["New Game", "Load Game", "Quit"]
        self.__current_choice = 0

    def update(self):
        #curses.clear()
        if UIManager.get_game() is not None:
            ScreenManager.change_screen(Screens.GAME)

        curses.mvaddstr(0,0,"coucou")
        for i, choice in enumerate(self.__choices):
            if i == self.__current_choice:
                curses.mvaddstr(i + 1, 1, f"> {choice}")
            else:
                curses.mvaddstr(i + 1, 1, f"  {choice}")
        curses.mvaddstr(0,0, "Main Menu")
        curses.refresh()

    def on_key(self, key):
        if key == curses.KEY_UP and self.__current_choice > 0:
            self.__current_choice -= 1
        elif key == curses.KEY_DOWN and self.__current_choice < len(self.__choices) - 1:
            self.__current_choice += 1
        # Check if key is the enter key of the keyboard or the enter key of the keypad
        elif key in (ord("\n"), 459):
            if self.__current_choice == 0:
                UIManager.change_ui(UIList.MENU)
                player1 = Player("Soufiane", "RED")
                player2 = Player("Bob", "GREEN")
                player3 = Player("Rémi", "MAGENTA")

                map = Map(120, 120, RessourceModes.GOLD_RUSH, PlayerModes.MARINES, {player1, player2})

                game = Game({player1, player2}, map)
                archer = Horseman(player1,Position(0, 0))
                map.add_unit(archer)
                game.add_action(MoveAction(map,archer, Position(10, 10)))

                UIManager.set_game(game)
                ScreenManager.change_screen(Screens.GAME)

            elif self.__current_choice == 1:
                ScreenManager.change_screen(Screens.SELECT_BACKUP)
            elif self.__current_choice == 2:
                UIManager.stop()
