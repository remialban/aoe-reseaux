from . import Unit


class Villager(Unit):
    def __init__(
        self,
        player,
        position,

    ):
        super().__init__(
            player,
            position,
            1,
            25,
            2,
            1,
            1,
            1,

        )

        self.max_stock = 25
        self.collect_speed = 25
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
