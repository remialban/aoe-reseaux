from core.resource import Resource
from core.utils import generate_id

class Unit:
    def __init__(
        self,
        player ,
        position,
        attack_speed: float,
        health_points: int,
        max_health_points: int,
        damage: int,
        movement_speed: float,
        range: float,
        training_time: float,
        cost: Resource,
    ):
        self.id = generate_id()
        self.attack_speed = attack_speed
        self.damage = damage
        self.health_points = health_points
        self.max_health_points = max_health_points
        self.movement_speed = movement_speed
        self.player = player
        self.position = position
        self.range = range
        self.training_time = training_time
        self.cost = cost
        self.owner = player.id


    def get_max_health_points(self):
        return self.max_health_points

    def attack_unit(self, unit):
        """Attacks another unit."""
        unit.remove_health_points(self.damage)
        print(
            f"{self.player.name} attacks {unit.player.name}'s unit causing {self.damage} damage."
        )

    def change_position(self, new_position):
        """Changes the unit's position on the map."""
        self.position = new_position
        # print(
        #     f"Unit moved to new position: {self.position.get_x()}, {self.position.get_y()}"
        # )

    def get_health_points(self):
        return self.health_points

    def get_max_health_points(self):
        return self.max_health_points

    def get_position(self):
        return self.position

    def get_player(self):
        return self.player

    def get_attack_speed(self):
        return self.attack_speed

    def get_damage(self):
        return self.damage

    def get_training_time(self):
        return self.training_time

    def get_map(self):
        return self.map

    def get_cost_resource(self):
        return self.cost

    def remove_health_points(self, hp):
        self.health_points -= hp
        if self.health_points <= 0:
            print(f"Unit from {self.player.name} has been destroyed.")

    def update(self):
        """Updates the unit’s status."""
        print(f"Unit belonging to {self.player.name} has been updated.")

    def attack_building(self, building):
        """Attacks a building."""
        building.remove_health_points(self.damage)
        print(
            f"{self.player.name}'s unit attacked a building causing {self.damage} damage."
        )

    def collect(self, farm):
        """Collects resources from a farm."""
        farm.collect_resources()
        print(f"Unit from {self.player.name} collected resources from the farm.")

    def get_movement_speed(self):
        return self.movement_speed

    def get_range(self):
        return self.range

    def __setattr__(self, key, value):
        from network.sender import Sender
        from network.state import State

        super().__setattr__(key, value)
        if not State.is_receiving() and self.__class__.__name__ != "Unit" and key not in ("id"):
            Sender.notify_edit(self, key, value)