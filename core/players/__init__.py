from core.resource import Resource
from core.utils import generate_id


class Player:
    def __init__(self, name: str, color: str, resource: Resource = Resource(0, 0, 0)):

        self.id = generate_id()
        self.name: str = name
        self.color: str = color
        self.stock: Resource = resource
        #Sender.notify_add(self)

        self.max_number_units: int = 0


    def get_color(self) -> str:
        return self.color

    def get_name(self) -> str:
        return self.name

    def get_max_number_units(self) -> int:
        return self.max_number_units

    def add_resources(self, resource: Resource):
        self.stock.add_food(resource.get_food())
        self.stock.add_wood(resource.get_wood())
        self.stock.add_gold(resource.get_gold())

    def get_stock(self) -> Resource:
        return self.stock

    def get_resource_to_collect(self):
        # returns "wood", "gold" or "food"
        # finds minimum between the three resources
        if self.stock.get_wood() < self.stock.get_gold():
            if self.stock.get_wood() < self.stock.get_food():
                return "wood"
            else:
                return "food"
        else:
            if self.stock.get_gold() < self.stock.get_food():
                return "gold"
            else:
                return "food"

    def __setattr__(self, key, value):
        from network.sender import Sender
        from network.state import State

        super().__setattr__(key, value)
        if not State.is_receiving() and key in ("max_number_units", "stock", "name", "color") and self.__class__.__name__ != "Player":
            Sender.notify_edit(self, key, value)
