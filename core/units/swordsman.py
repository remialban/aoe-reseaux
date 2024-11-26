from . import Unit


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
            damage=4,
            movement_speed=0.9,
            range=0.40,
            training_time=20,
        )
