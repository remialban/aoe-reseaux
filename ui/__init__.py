from abc import abstractmethod


class UI:
    """ Abstract class for UIs """
    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def loop(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass