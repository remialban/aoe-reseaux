from . import Unit
from core.resource import Resource


class Horseman(Unit):
    def __init__(
        self,
        player,
        position,
    ):
        super().__init__(
            player,
            position,
            attack_speed=1,
            health_points=45,
            max_health_points=45,
            damage=4,
            movement_speed=1.2,
            range=0.38,
            training_time=30,
            cost=Resource(0, 20, 80),
        )
