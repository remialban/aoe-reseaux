from core.resource import Resource


class Player:
    def __init__(self, name: str, color: str):
        self.name: str = name
        self.color: str = color
        self.max_number_units: int = 0
        self.stock: Resource = Resource()


    def get_color(self) -> str:
        return self.color

    def get_name(self) -> str:
        return self.name

    def get_max_number_units(self) -> int:
        return self.max_number_units
    """
    def calculate_max_number_units(self) -> int:
        House_count = sum(1 for building in self.buildings if building.building_type == "House")
        TownCenter_count = sum(1 for building in self.buildings if building.building_type == "TownCenter")
    
        # calculation: each house allows 10 units
        self.max_number_units = House_count * 5 + TownCenter_count * 5
        return self.max_number_units
    """