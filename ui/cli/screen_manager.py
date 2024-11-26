import unicurses as curses

from ui.cli.enum import Screens
from ui.cli.screens import Screen
from ui.enums import UIList
from ui.ui_manager import UIManager


class ScreenManager:
    __screens: dict[Screens, Screen] = {}
    __current_screen: Screen|None = None

    __window = None

    @staticmethod
    def add_screen(name: Screens, screen: Screen):
        ScreenManager.__screens[name] = screen
        if ScreenManager.__current_screen is None:
            ScreenManager.__current_screen = screen

    @staticmethod
    def change_screen(name: Screens):
        ScreenManager.__current_screen = ScreenManager.__screens[name]
        if ScreenManager.__window is not None:
            curses.clear()

    @staticmethod
    def loop(window):
        ScreenManager.__window = window
        while ScreenManager.__current_screen is not None:
            key = curses.getch()
            if key != -1:
                if key == curses.KEY_F(12):
                    UIManager.change_ui(UIList.GUI)
                ScreenManager.__current_screen.on_key(key)
            ScreenManager.__current_screen.update()
            curses.refresh()
            if UIManager.get_game() is not None:
                UIManager.get_game().party()
