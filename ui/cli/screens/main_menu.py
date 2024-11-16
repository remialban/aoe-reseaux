import curses

from ui.cli import Screen, GameMenu, ScreenManager, Screens
from ui.ui_manager import UIManager


class MainMenu(Screen):
    def __init__(self, window: curses.window):
        super().__init__(window)
        self.__choices = ["New Game", "Load Game", "Quit"]
        self.__current_choice = 0

    def update(self):
        self._window.clear()
        for i, choice in enumerate(self.__choices):
            if i == self.__current_choice:
                self._window.addstr(i + 1, 1, f"> {choice}")
            else:
                self._window.addstr(i + 1, 1, f"  {choice}")

    def on_key(self, key):
        if key == curses.KEY_UP and self.__current_choice > 0:
            self.__current_choice -= 1
        elif key == curses.KEY_DOWN and self.__current_choice < len(self.__choices) - 1:
            self.__current_choice += 1
        elif key == ord("\n"):
            if self.__current_choice == 0:
                pass
            elif self.__current_choice == 1:
                ScreenManager.change_screen(Screens.SELECT_BACKUP)
            elif self.__current_choice == 2:
                UIManager.stop()
