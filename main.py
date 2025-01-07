from ui.cli import CLI
from ui.enums import UIList
from ui.gui import GUI
from ui.ui_manager import UIManager


def main():
    UIManager.add_ui(UIList.CLI, CLI())

    UIManager.add_ui(UIList.GUI, GUI())

    UIManager.loop()

if __name__ == "__main__":
    main()