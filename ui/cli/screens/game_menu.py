import unicurses as curses

from ui.cli import Screen, ScreenManager, Screens
from ui.ui_manager import UIManager


class GameMenu(Screen):
    def __init__(self, window):
        super().__init__(window)
        self.__choices = ["Resume", "Save", "Quit"]
        self.__current_choice = 0
        self.message = ""


    def update(self):
        curses.clear()
        for i, choice in enumerate(self.__choices):
            if i == self.__current_choice:
                curses.mvaddstr(i + 1, 1, f"> {choice}")
            else:
                curses.mvaddstr(i + 1, 1, f"  {choice}")

        curses.mvaddstr(5, 1, self.message)


    def on_key(self, key):
        if key == curses.KEY_UP and self.__current_choice > 0:
            self.__current_choice -= 1
            self.message = ""
        elif key == curses.KEY_DOWN and self.__current_choice < len(self.__choices) - 1:
            self.__current_choice += 1
            self.message = ""
        # Check if key is the enter key of the keyboard or the enter key of the keypad
        elif key in (ord("\n"), 459):
            if self.__current_choice == 0:
                UIManager.stop_game()
                ScreenManager.change_screen(Screens.GAME)
            elif self.__current_choice == 1:
                try:
                    UIManager.save_game(UIManager.get_name())
                    self.message = "Game saved"
                except Exception as e:
                    curses.mvaddstr(1, 1, f"Error: {e}")
                    self.message = "Erreur lors de la sauvegarde"
            elif self.__current_choice == 2:
                UIManager.set_game(None)
                ScreenManager.change_screen(Screens.MENU)

