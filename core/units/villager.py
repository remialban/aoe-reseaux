from . import Unit


class Villager(Unit):
    def __init__(
        self,
        player,
        map,
        position,
        attack_speed: float,
        health_points: int,
        damage: int,
        movement_speed: float,
        range: float,
        training_time: float,
        max_stock: int,
    ):
        super().__init__(
            player,
            map,
            position,
            attack_speed,
            health_points,
            damage,
            movement_speed,
            range,
            training_time,
        )
        self.max_stock = max_stock
        self.stock = {}

    def build(self, building):
        """Builds a structure."""
        print(f"Villager from {self.player.name} is building {building}.")
        # Logic for building

    def collect_resources(self, resource_type, amount):
        """Collects resources for the player."""
        if resource_type not in self.stock:
            self.stock[resource_type] = 0
        self.stock[resource_type] += amount
        print(
            f"Villager from {self.player.name} collected {amount} of {resource_type}."
        )
    def get_max_stock(self):
        return self.max_stock

    def get_stock(self):
        return self.stock