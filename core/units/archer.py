from . import Unit
from core.resource import Resource


class Archer(Unit):
    def __init__(
        self,
        player,
        position,
    ):
        super().__init__(
            player,
            position,
            attack_speed=1,
            health_points=30,
            max_health_points=30,
            damage=4,
            movement_speed=1,
            range=4,
            training_time=35,
            cost=Resource(25, 45, 0),
        )
