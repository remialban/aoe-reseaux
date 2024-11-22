import unicurses as curses
from abc import abstractmethod


class Screen:
    def __init__(self, window):
        self._window = window

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def on_key(self, key):
        pass
