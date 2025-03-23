import threading


class State:
    __is_receiving = False

    @staticmethod
    def is_receiving():
        return State.__is_receiving

    @staticmethod
    def set_receiving(is_receiving):
        State.__is_receiving = is_receiving


    lock = threading.Lock()


