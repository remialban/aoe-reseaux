import unicurses as curses

from ui import UI
from ui.cli.enum import Screens
from ui.cli.screen_manager import ScreenManager
from ui.cli.screens import Screen
from ui.cli.screens.game_menu import GameMenu
from ui.cli.screens.game_screen import GameScreen
from ui.cli.screens.main_menu import MainMenu
from ui.cli.screens.select_backup import SelectBackup


class CLI(UI):
    def setup(self):
        pass

    def run(self):
        window = curses.initscr()
        curses.curs_set(0)
        curses.keypad(window, True)
        curses.nodelay(window, 1)
        curses.timeout(500)
        curses.start_color()

        ScreenManager.add_screen(Screens.MENU, MainMenu(window))
        ScreenManager.add_screen(Screens.GAME, GameScreen(window))

        ScreenManager.add_screen(Screens.GAME_MENU, GameMenu(window))
        ScreenManager.add_screen(Screens.SELECT_BACKUP, SelectBackup(window))

        ScreenManager.loop(window)

    def loop(self):
        self.run()

    def cleanup(self):
        curses.endwin()