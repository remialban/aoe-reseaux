import curses

from ui import UI
from ui.cli.enum import Screens
from ui.cli.screen_manager import ScreenManager
from ui.cli.screens import Screen
from ui.cli.screens.game_screen import GameScreen


class CLI(UI):
    def setup(self):
        pass

    def run(self, window: curses.window):
        curses.initscr()
        curses.curs_set(0)
        window.nodelay(1)
        window.timeout(500)

        ScreenManager.add_screen(Screens.GAME, GameScreen(window))
        ScreenManager.loop(window)

    def loop(self):
        curses.wrapper(self.run)

    def cleanup(self):
        pass