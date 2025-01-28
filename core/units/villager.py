from . import Unit
from core.resource import Resource


class Villager(Unit):
    def __init__(
        self,
        player,
        position,
    ):
        super().__init__(
            player,
            position,
            attack_speed=1,
            health_points=25,
            max_health_points=25,
            damage=2,
            movement_speed=1,
            range=1,
            training_time=25,
            cost=Resource(0, 0, 50),
        )

        self.max_stock = 20
        self.collect_speed = 25
        self.stock = {
            "gold": 0,
            "wood": 0,
            "food": 0,
        }

    def build(self, building):
        """Builds a structure."""
        # print(f"Villager from {self.player.name} is building {building}.")
        # Logic for building

    def collect_resources(self, resource_type, amount):
        """Collects resources for the player."""
        if resource_type not in self.stock:
            self.stock[resource_type] = 0
        self.stock[resource_type] += amount
        # print(
        #     f"Villager from {self.player.name} collected {amount} of {resource_type}."
        # )

    def remove_resources(self, resource_type, amount):
        """Removes resources from the player."""
        if resource_type not in self.stock:
            self.stock[resource_type] = 0
        self.stock[resource_type] -= amount
        # print(
        #     f"Villager from {self.player.name} removed {amount} of {resource_type}."
        # )

    def get_max_stock(self):
        return self.max_stock

    def get_stock(self):
        return self.stock
