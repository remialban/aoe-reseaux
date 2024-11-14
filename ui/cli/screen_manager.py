import curses

from ui.cli.enum import Screens
from ui.cli.screens import Screen


class ScreenManager:
    __screens: dict[Screens, Screen] = {}
    __current_screen: Screen|None = None

    __window: curses.window|None = None

    @staticmethod
    def add_screen(name: Screens, screen: Screen):
        ScreenManager.__screens[name] = screen
        if ScreenManager.__current_screen is None:
            ScreenManager.__current_screen = screen

    @staticmethod
    def change_screen(name: Screens):
        ScreenManager.__current_screen = ScreenManager.__screens[name]
        if ScreenManager.__window is not None:
            ScreenManager.__window.clear()

    @staticmethod
    def loop(window: curses.window):
        ScreenManager.__window = window
        while ScreenManager.__current_screen is not None:
            key = window.getch()
            if key != -1:
                ScreenManager.__current_screen.on_key(key)
            ScreenManager.__current_screen.update()
            window.refresh()
            window.timeout(10000)
