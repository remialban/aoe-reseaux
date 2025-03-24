from core.position import Position

from core.resource import Resource
from core.utils import generate_id


class ResourcePoint:
    __position: Position
    __resources: Resource
    __owner : int

    def __init__(self, position: Position, resource: Resource, owner ) -> None:
        self.id = generate_id()
        self.__position = position
        self.__resources = resource
        self.__owner = owner.id

    def get_resources(self) -> Resource:
        return self.__resources

    def get_position(self) -> Position:
        return self.__position

    def get_resource(self):
        return self.__resources

    def collect(self, amount: float, max_stock: int, stock: Resource):

        if stock.get_food() + stock.get_wood() + stock.get_gold() + amount <= max_stock:
            assert amount > 0, amount

            if (
                self.__resources.get_gold() > 0
                and self.__resources.get_food() == 0
                and self.__resources.get_wood() == 0
            ):
                assert amount <= self.__resources.get_gold(), amount
                self.__resources.remove_gold(amount)
                stock.add_gold(amount)
                return 2

            elif (
                self.__resources.get_wood() > 0
                and self.__resources.get_food() == 0
                and self.__resources.get_gold() == 0
            ):
                assert amount <= self.__resources.get_wood(), amount
                self.__resources.remove_wood(amount)
                print("Wood: ", self.__resources.get_wood())
                stock.add_wood(amount)
                return 1

            else:
                return -1
        else:
            return 0

    def __setattr__(self, key, value):
        from network.sender import Sender
        from network.state import State

        super().__setattr__(key, value)
        if not State.is_receiving():
            Sender.notify_edit(self, key, value)