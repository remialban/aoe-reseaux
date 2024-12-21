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
            attack_speed=1,
            health_points=25,
            max_health_points=25,
            damage=2,
            mouvement_speed=1,
            range=1,
            training_time=25,

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
