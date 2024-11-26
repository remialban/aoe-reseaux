import unicurses as curses

from core import Player, Map, Game
from ui.cli import Screen, GameMenu, ScreenManager, Screens
from ui.ui_manager import UIManager


class MainMenu(Screen):
    def __init__(self, window):
        super().__init__(window)
        self.__choices = ["New Game", "Load Game", "Quit"]
        self.__current_choice = 0

    def update(self):
        #curses.clear()
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
                player1 = Player("Alice", "RED")
                player2 = Player("Bob", "GREEN")

                map = Map(100, 100)

                game = Game({player1, player2}, map)

                UIManager.set_game(game)
                ScreenManager.change_screen(Screens.GAME)

            elif self.__current_choice == 1:
                ScreenManager.change_screen(Screens.SELECT_BACKUP)
            elif self.__current_choice == 2:
                UIManager.stop()
