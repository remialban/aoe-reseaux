import unicurses as curses

from core.buildings.archery_range import ArcheryRange
from core.buildings.barracks import Barracks
from core.buildings.camp import Camp
from core.buildings.farm import Farm
from core.buildings.house import House
from core.buildings.keep import Keep
from core.buildings.stable import Stable
from core.buildings.town_center import TownCenter
from core.resources_points.mine import Mine
from core.resources_points.wood import Wood
from core.units.archer import Archer
from core.units.horse_man import Horseman
from core.units.swordsman import Swordsman
from core.units.villager import Villager
from ui.cli import Screens, ScreenManager
from ui.cli.screens import Screen
from ui.ui_manager import UIManager
import keyboard

class GameScreen(Screen):
    UNIT_REPRESENTATION: dict[type, str] = {
        Archer: "a",
        Horseman: "h",
        Swordsman: "s",
        Villager: "v"
    }

    BUILDING_REPRESENTATION: dict[type, str] = {
        ArcheryRange: "A",
        Barracks: "B",
        Camp: "C",
        Farm: "F",
        House: "H",
        Keep: "K",
        Stable: "S",
        TownCenter: "T"
    }

    SOURCE_POINT_REPRESENTATION: dict[type, str] = {
        Mine: "M",
        Wood: "W"
    }

    COLORS: dict[str, int] = {
        "RED": 1,
        "GREEN": 2,
        "YELLOW": 3,
        "BLUE": 4,
        "MAGENTA": 5,
        "CYAN": 6,
        "WHITE": 7
    }
    def __init__(self, window):
        super().__init__(window)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.__camera = [0, 0]

    def check_if_position_in_camera(self, x, y):
        height, width = curses.getmaxyx(self._window)
        # use self.__camera to check if the position is in the camera
        return 0 <= y - self.__camera[1] + 1 < height and 0 <= x - self.__camera[0] + 1 < width

    def new_coordonates(self, x, y):
        return x - self.__camera[0] + 1, y - self.__camera[1] + 1


    def update(self):
        curses.clear()
        game = UIManager.get_game()

        height, width = curses.getmaxyx(self._window)

        # Show Left border
        for i in range(UIManager.get_game().get_map().get_height() + 2):
            x = 0
            if self.check_if_position_in_camera(x-1, i-1):
                new_coordonates = self.new_coordonates(x-1, i-1)
                curses.mvaddstr(new_coordonates[1], new_coordonates[0], "#")

        # Show bottom border
        for i in range(UIManager.get_game().get_map().get_width() + 2):
            y = UIManager.get_game().get_map().get_height()
            if self.check_if_position_in_camera(i-1, y):
                new_coordonates = self.new_coordonates(i-1, y)
                curses.mvaddstr(new_coordonates[1], new_coordonates[0], "#")

        # Show right border
        for i in range(UIManager.get_game().get_map().get_height() + 1):
            x = UIManager.get_game().get_map().get_width()
            if self.check_if_position_in_camera(x, i-1):
                new_coordonates = self.new_coordonates(x, i-1)
                curses.mvaddstr(new_coordonates[1], new_coordonates[0], "#")

        # Show top border
        for i in range(UIManager.get_game().get_map().get_width() + 2):
            y = 0
            if self.check_if_position_in_camera(i - 1, y - 1):
                new_coordonates = self.new_coordonates(i - 1, y - 1)
                curses.mvaddstr(new_coordonates[1], new_coordonates[0], "#")

        # Show buildings
        for building in game.get_map().get_buildings():
            for i in range(building.get_width()):
                for j in range(building.get_height()):
                    new_x = building.get_position().get_x() + i
                    new_y = building.get_position().get_y() + j
                    new_coordonates = self.new_coordonates(new_x, new_y)
                    if self.check_if_position_in_camera(new_x, new_y):
                        curses.mvaddstr(int(new_coordonates[1]), int(new_coordonates[0]), GameScreen.BUILDING_REPRESENTATION.get(type(building), "B"), curses.color_pair(GameScreen.COLORS.get(building.get_player().get_color(), 0)))
        # Show resources points
        for resource in game.get_map().get_resources():
            x, y = resource.get_position().get_x(), resource.get_position().get_y()
            if self.check_if_position_in_camera(x, y):
                new_coordonates = self.new_coordonates(x, y)
                curses.mvaddstr(int(new_coordonates[1]), int(new_coordonates[0]), GameScreen.SOURCE_POINT_REPRESENTATION.get(type(resource), "R"), curses.color_pair(7))

        # Show units
        for unit in game.get_map().get_units():
            x, y = unit.get_position().get_x(), unit.get_position().get_y()
            if self.check_if_position_in_camera(x, y):
                new_coordonates = self.new_coordonates(x, y)
                curses.mvaddstr(int(new_coordonates[1]), int(new_coordonates[0]),
                                    GameScreen.UNIT_REPRESENTATION.get(type(unit), "u"),
                                    curses.color_pair(GameScreen.COLORS.get(unit.get_player().get_color(), 0)))

    def on_key(self, key):
        if keyboard.is_pressed("shift"):
            self.offset = 10
        else:
            self.offset = 1
        offset = self.offset

        if (keyboard.is_pressed("z") or keyboard.is_pressed("up")) and self.__camera[1] > 0:
            self.__camera[1] -= offset
        elif (keyboard.is_pressed("s") or keyboard.is_pressed("down")):
            self.__camera[1] += offset
        elif (keyboard.is_pressed("q") or keyboard.is_pressed("left")) and self.__camera[0] > 0:
            self.__camera[0] -= offset
        elif (keyboard.is_pressed("d") or keyboard.is_pressed("right")):
            self.__camera[0] += offset

        # if key in (curses.KEY_UP, ord('z')) and self.__camera[1] > 0:
        #     self.__camera[1] -= offset
        # elif key in (curses.KEY_DOWN, ord('s')):
        #     self.__camera[1] += offset
        # elif key in (curses.KEY_LEFT, ord('q')) and self.__camera[0] > 0:
        #     self.__camera[0] -= offset
        # elif key in (curses.KEY_RIGHT, ord('d')):
        #     self.__camera[0] += offset
        # elif key == 27:
        #     ScreenManager.change_screen(Screens.GAME_MENU)

