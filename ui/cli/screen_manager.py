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
                if key == curses.KEY_F(9):
                    if UIManager.get_game() is None:
                        UIManager.change_ui(UIList.MENU)
                    else:
                        UIManager.change_ui(UIList.GUI)
                elif key == curses.KEY_F(1) and UIManager.get_game() is not None:
                    UIManager.render_html()
                elif key == ord("p") and UIManager.get_game() is not None and not UIManager.get_game().is_paused():
                    UIManager.get_game().pause()
                    UIManager.stop_game()
                elif key == ord("r") and UIManager.get_game() is not None and UIManager.get_game().is_paused():
                    UIManager.get_game().resume()
                    UIManager.start_game()
                elif key == ord("\t"):
                    UIManager.get_game().pause()
                    UIManager.stop_game()
                    UIManager.render_html()
                    UIManager.open_in_browser()
                elif key == curses.KEY_F(12):
                    ScreenManager.change_screen(Screens.SELECT_BACKUP)
                elif key == curses.KEY_F(11) and UIManager.get_game() is not None:
                    UIManager.save_game(UIManager.get_name())
                ScreenManager.__current_screen.on_key(key)
            try:
                ScreenManager.__current_screen.update()
            except:
                pass
            curses.refresh()
            if UIManager.get_game() is not None:
                #UIManager.get_game().party()
                UIManager.start_game()

