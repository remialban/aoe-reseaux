import curses

from ui.cli import Screen, ScreenManager, Screens
from ui.ui_manager import UIManager


class SelectBackup(Screen):
    def __init__(self, window:  curses.window):
        super().__init__(window)
        self.__choices = UIManager.get_backups()
        self.__choices.sort(reverse=True)
        self.__current_choice = 0
        self.__offset = 0

    def update(self):
        # Show the list of backups with offset (camera) and the height of the window
        self._window.clear()
        self._window.refresh()
        height, width = self._window.getmaxyx()

        for i, choice in enumerate(self.__choices[self.__offset:self.__offset + height - 2]):
            if i == self.__current_choice - self.__offset:
                self._window.addstr(i + 1, 1, f"> [{self.__offset + i}] {choice}")
            else:
                self._window.addstr(i + 1, 1, f"  [{self.__offset + i}] {choice}")

    def on_key(self, key):
        height, width = self._window.getmaxyx()

        if key == curses.KEY_UP and self.__current_choice > 0:
            self.__current_choice -= 1
            if self.__current_choice < self.__offset:
                self.__offset -= 1
        elif key == curses.KEY_DOWN and self.__current_choice < len(self.__choices) - 1:
            self.__current_choice += 1
            if self.__current_choice >= self.__offset + height - 2:
                self.__offset += 1
        elif key == ord("\n"):
            UIManager.load_game(self.__choices[self.__current_choice])
            ScreenManager.change_screen(Screens.GAME)
        elif key == 27:
            ScreenManager.change_screen(Screens.MENU)