from enum import EnumType


class Screens(EnumType):
    MAIN_MENU = 1
    MAP = 2
    PAUSE_MENU = 3

class ScreenManager:
    __screens = {}
    __current_screen = None

    @staticmethod
    def change_screen(screen_name: Screens):
        if ScreenManager.__current_screen is not None:
            ScreenManager.__current_screen.cleanup()

        ScreenManager.__current_screen = ScreenManager.__screens.get(screen_name, None)
        if ScreenManager.__current_screen is not None:
            ScreenManager.__current_screen.setup()

    @staticmethod
    def add_screen(name: Screens, screen):
        ScreenManager.__screens[name] = screen

    @staticmethod
    def loop():
        while ScreenManager.__current_screen is not None:
            ScreenManager.__current_screen.loop()