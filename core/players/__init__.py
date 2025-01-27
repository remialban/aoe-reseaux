from core.resource import Resource


class Player:
    def __init__(self, name: str, color: str, resource: Resource = Resource(0, 0, 0)):
        self.name: str = name
        self.color: str = color
        self.max_number_units: int = 0
        self.stock: Resource = resource

    def get_color(self) -> str:
        return self.color

    def get_name(self) -> str:
        return self.name

    def get_max_number_units(self) -> int:
        return self.max_number_units
