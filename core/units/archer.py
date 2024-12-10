from . import Unit


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
        )
