from core import Player, TownCenter, AI
from core.position import Position
from core.resource import Resource
from core.units.archer import Archer
from network.receiver import Receiver
from network.sender import Sender
from network.state import State
from tests.test_resource import resource
from ui.cli import CLI
from ui.enums import UIList
from ui.gui import GUI
from ui.menu import MENU
from ui.ui_manager import UIManager


def main():
    UIManager.add_ui(UIList.MENU, MENU())

    UIManager.add_ui(UIList.CLI, CLI())

    UIManager.add_ui(UIList.GUI, GUI())
    Receiver.init(UIManager)
    #UIManager.change_ui(UIList.MENU)


    UIManager.loop()

if __name__ == "__main__":
    State.set_receiving(False)
    # p = AI("test", "red")
    # State.set_receiving(False)
    #
    # p.name = "Rémi"
    #
    # u = Archer(p, Position(10,20))
    # u.health_points = 20
    # exit(0)
    main()