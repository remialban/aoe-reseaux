from . import Unit
from core.resource import Resource


class Swordsman(Unit):
    def __init__(
        self,
        player,
        position,
    ):
        super().__init__(
            player,
            position,
            attack_speed=1,
            health_points=40,
            max_health_points=40,
            damage=4,
            movement_speed=0.9,
            range=1,
            training_time=20,
            cost=Resource(0, 20, 50),
        )
