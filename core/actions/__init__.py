from abc import ABC, abstractmethod

class Action(ABC) :

    @abstractmethod
    def do_action(self):
        pass

