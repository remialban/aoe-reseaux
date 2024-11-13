from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Action(ABC) :

    __old_time : datetime
    __new_time : datetime
    @abstractmethod
    def do_action(self)->bool:
        pass

    def before_action(self):
        self.__new_time = datetime.now()

    def after_action(self):
        self.__old_time = self.__new_time

    def __init__(self):
        self.before_action()
        self.__old_time = (self.__new_time + timedelta(seconds = -80))

    def get_old_time(self):
        return self.__old_time

    def get_new_time(self):
        return self.__new_time
