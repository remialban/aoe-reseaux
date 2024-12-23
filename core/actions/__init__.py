from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Action(ABC) :

    __old_time : datetime
    __new_time : datetime
    __saved_time_delta : timedelta
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

    def save_time_delta(self):
        self.__saved_time_delta = self.__new_time - self.__old_time

    def get_saved_time_delta(self):
        return self.__saved_time_delta

    def set_old_time(self, t : datetime):
        self.__old_time = t

