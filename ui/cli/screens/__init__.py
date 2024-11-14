import curses
from abc import abstractmethod


class Screen:
    def __init__(self, window: curses.window):
        self._window = window

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def on_key(self, key):
        pass
