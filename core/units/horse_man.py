from . import Unit


class Horseman(Unit):
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
