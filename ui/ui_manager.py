import os.path

from core import Game
from ui import UI
from ui.enums import UIList
from datetime import datetime
import pickle


class UIException(Exception):
    def __init__(self, ui: UI):
        super().__init__("UI closed")
        self.__ui = ui

    def get_ui(self):
        return self.__ui

class UIManager:
    __uis: dict[UIList, UI] = {}
    __current_ui: UI|None = None

    __game: Game|None = None

    @staticmethod
    def add_ui(name: UIList, ui: UI):
        UIManager.__uis[name] = ui
        if UIManager.__current_ui is None:
            UIManager.__current_ui = ui

    @staticmethod
    def change_ui(name: UIList|None):
        old_ui: UI = UIManager.__current_ui
        UIManager.__current_ui = UIManager.__uis.get(name, None)

        if UIManager.__current_ui is not None:
            UIManager.__current_ui.setup()

        raise UIException(old_ui)

    @staticmethod
    def stop():
        UIManager.change_ui(None)

    @staticmethod
    def loop():
        while UIManager.__current_ui is not None:
            try:
                UIManager.__current_ui.loop()
            except UIException as e:
                e.get_ui().cleanup()

    @staticmethod
    def get_name():
        return datetime.now().strftime("backup_%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_game(self):
        return UIManager.__game

    @staticmethod
    def load_game(filename: str):
        file = open(filename, "rb")
        UIManager.__game = pickle.load(file)
        file.close()

    @staticmethod
    def save_game(filename: str):
        if os.path.exists(filename):
            if os.path.isfile(filename):
                os.remove(filename)
            else:
                raise Exception("File already exists and is not a file")

        file = open(filename, "wb")
        pickle.dump(UIManager.__game, file)
        file.close()

