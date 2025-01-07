import os.path

from jinja2 import Environment, FileSystemLoader

from core import Game
from ui import UI
from ui.enums import UIList
from datetime import datetime
import pickle


class UIException(Exception):
    """
    Exception raised when a UI is closed
    """
    def __init__(self, ui: UI):
        super().__init__("UI closed")
        self.__ui = ui

    def get_ui(self):
        return self.__ui

class UIManager:
    """
    Class managing the UIs
    This class allows to change the current UI, add a new UI, stop the current UI and loop over the current UI
    Also allow to set game, load game, save game and get backups
    """
    __uis: dict[UIList, UI] = {}
    __current_ui: UI|None = None

    __game: Game|None = None

    @staticmethod
    def add_ui(name: UIList, ui: UI):
        UIManager.__uis[name] = ui
        if UIManager.__current_ui is None:
            UIManager.__current_ui = ui
            UIManager.__current_ui.setup()

    @staticmethod
    def get_current_ui() -> UI:
        return UIManager.__current_ui

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
                print("ccccccc")
            except UIException as e:
                e.get_ui().cleanup()
            except e:
                exit()

    @staticmethod
    def get_name():
        return datetime.now().strftime("backup_%Y-%m-%d_%H_%M_%S")

    @staticmethod
    def get_game() -> Game:
        """
        Get the current game
        :return:
        """
        return UIManager.__game

    @staticmethod
    def set_game(game: Game):
        """
        Set the current game
        :param game: the game
        :return:
        """
        UIManager.__game = game

    @staticmethod
    def load_game(filename: str):
        """
        Load a game from a file
        :param filename: the filename
        """
        file = open(f"backups/{filename}", "rb")
        UIManager.__game = pickle.load(file)
        file.close()

    @staticmethod
    def save_game(filename: str):
        """
        Save the current game to a file
        :param filename:
        :return:
        """
        if os.path.exists(filename):
            if os.path.isfile(filename):
                os.remove(filename)
            else:
                raise Exception("File already exists and is not a file")
        new_filename = f"backups/{filename}"
        file = open(new_filename, "wb")
        pickle.dump(UIManager.__game, file)
        file.close()

    @staticmethod
    def get_backups():
        if not os.path.exists("backups"):
            os.mkdir("backups")
        return [f for f in os.listdir("backups") if os.path.isfile(f"backups/{f}") and f.startswith("backup_")]

    @staticmethod
    def render_html():
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('template.html')

        players = sorted(list(UIManager.__game.get_players()), key= lambda obj: obj.get_color())
        tab = []
        for player in players:
            dictionnaire = {}
            units =  list(UIManager.__game.get_map().get_units(player))
            dictionnaire["units"] = sorted(units, key= lambda obj: str(type(obj)))

            buildings = list(UIManager.__game.get_map().get_buildings(player))
            dictionnaire["buildings"] = sorted(buildings, key= lambda obj: str(type(obj)))

            units_classes = {type(unit).__name__ for unit in units}
            units_stats = {}
            for unit_class in units_classes:
                units_stats[unit_class] = len([unit for unit in units if type(unit).__name__ == unit_class])

            dictionnaire["stats"] = {
                "units_number": len(units),
                "buildings_number": len(buildings),
                "units_stats": units_stats

            }
            tab.append(dictionnaire)

        data = {
            "game": UIManager.__game,
            "players": players,
            "units": [unit for unit in UIManager.__game.get_players()],
            "entities": tab,
            "stats": units_stats
        }

        rendered_html = template.render(data)
        with open("game.html", "w") as file:
            file.write(rendered_html)
