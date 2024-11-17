import curses

from ui.cli import Screen, ScreenManager, Screens
from ui.ui_manager import UIManager


class GameMenu(Screen):
    def __init__(self, window):
        super().__init__(window)
        self.__choices = ["Resume", "Save", "Quit"]
        self.__current_choice = 0
        self.message = ""


    def update(self):
        self._window.clear()
        for i, choice in enumerate(self.__choices):
            if i == self.__current_choice:
                self._window.addstr(i + 1, 1, f"> {choice}")
            else:
                self._window.addstr(i + 1, 1, f"  {choice}")

        self._window.addstr(5, 1, self.message)


    def on_key(self, key):
        if key == curses.KEY_UP and self.__current_choice > 0:
            self.__current_choice -= 1
            self.message = ""
        elif key == curses.KEY_DOWN and self.__current_choice < len(self.__choices) - 1:
            self.__current_choice += 1
            self.message = ""
        elif key == ord("\n"):
            if self.__current_choice == 0:
                ScreenManager.change_screen(Screens.GAME)
            elif self.__current_choice == 1:
                try:
                    UIManager.save_game(UIManager.get_name())
                    self.message = "Game saved"
                except Exception as e:
                    self._window.addstr(1, 1, f"Error: {e}")
                    self.message = "Erreur lors de la sauvegarde"
            elif self.__current_choice == 2:
                ScreenManager.change_screen(Screens.MENU)

