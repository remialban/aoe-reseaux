from abc import abstractmethod

import pygame


class Screen:
    def __init__(self, window: pygame.Surface):
        self._window = window

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass