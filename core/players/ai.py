from core.actions import AttackBuildingAction, AttackUnitAction, MoveAction, CollectAction
from core.actions import BuildAction, TrainAction
from core.units.villager import Villager
from core.units.archer import Archer
from core.units.horse_man import Horseman
from core.units.swordsman import Swordsman
from core.buildings import Keep, Farm, TownCenter, Barracks, Stable, ArcheryRange, House


class AI:
    def __init__(self, name, strategy="balanced"):
        self.name = name
        self.strategy = strategy  # Can be "defensive", "aggressive", or "balanced"

    def play(self, game_state):
        if self.strategy == "defensive":
            self.defensive_strategy(game_state)
        elif self.strategy == "aggressive":
            self.aggressive_strategy(game_state)
        elif self.strategy == "balanced":
            self.balanced_strategy(game_state)

    def defensive_strategy(self, game_state):
        """Focuses on defense: builds defensive structures and trains defensive units."""
        for building in game_state.get_buildings(self):
            if isinstance(building, TownCenter):
                self.train_unit(Villager, building, game_state)

        if self.needs_defense(game_state):
            self.build_structure(Keep, game_state)

        self.manage_economy(game_state)

    def aggressive_strategy(self, game_state):
        """Focuses on attacking: trains attack units and launches attacks."""
        for building in game_state.get_buildings(self):
            if isinstance(building, Barracks):
                self.train_unit(Swordsman, building, game_state)
            elif isinstance(building, ArcheryRange):
                self.train_unit(Archer, building, game_state)
            elif isinstance(building, Stable):
                self.train_unit(Horseman, building, game_state)

        self.launch_attack(game_state)
        self.manage_economy(game_state)

    def balanced_strategy(self, game_state):
        """Balances between attack and defense based on the situation."""
        if self.needs_defense(game_state):
            self.defensive_strategy(game_state)
        else:
            self.aggressive_strategy(game_state)

    def train_unit(self, unit_type, building, game_state):
        """Trains a unit of the given type at the specified building."""
        if self.can_train(building, unit_type):
            action = TrainAction(self, building, unit_type)
            if self.has_resources_for(unit_type):
                game_state.add_action(action)
                self.deduct_resources_for(unit_type)

    def can_train(self, building, unit_type):
        """Determines if a building can train a specific unit type."""
        return (
            building.is_training_ready() and unit_type in building.get_trainable_units()
        )

    def build_structure(self, structure_type, game_state):
        """Builds a structure of the given type if resources allow."""
        if self.has_resources_for(structure_type):
            action = BuildAction(self, structure_type)
            game_state.add_action(action)
            self.deduct_resources_for(structure_type)

    def manage_economy(self, game_state):
        """Ensures sufficient resources by building Farms and Houses as needed."""
        if self.needs_more_houses(game_state):
            self.build_structure(House, game_state)

        if self.needs_more_food(game_state):
            self.build_structure(Farm, game_state)

        self.collect_resources(game_state)

    def needs_more_houses(self, game_state):
        """Checks if the AI needs more Houses to support population growth."""
        current_population = game_state.get_current_population(self)
        max_population = game_state.get_max_population(self)
        return current_population >= max_population

    def needs_more_food(self, game_state):
        """Checks if the AI needs more Farms to sustain food production."""
        return self.get_resources().get_food() < 50  # Example threshold

    def collect_resources(self, game_state):
        """Directs villagers to collect resources using CollectAction."""
        for unit in game_state.get_units(self):
            if isinstance(unit, Villager):
                resource_point = self.find_closest_resource(game_state, unit)
                if resource_point:
                    self.move_to_collect(unit, resource_point, game_state)

    def move_to_collect(self, unit, resource_point, game_state):
        """Moves a unit to the resource point and collects resources."""
        if not self.is_position_available(resource_point.get_position(), game_state):
            alternative_resource = self.find_alternative_resource(game_state, unit)
            if alternative_resource:
                resource_point = alternative_resource

        if unit.get_position() != resource_point.get_position():
            move_action = MoveAction(
                game_state.get_map(), unit, resource_point.get_position()
            )
            game_state.add_action(move_action)

        collect_action = CollectAction(unit, resource_point)
        game_state.add_action(collect_action)

    def is_position_available(self, position, game_state):
        """Checks if the given position is available for a unit to move to."""
        for building in game_state.get_buildings():
            if building.get_position() == position:
                return building.is_walkable()
        for unit in game_state.get_units():
            if unit.get_position() == position:
                return False
        return True

    def find_alternative_resource(self, game_state, unit):
        """Finds an alternative resource point if the closest one is not accessible."""
        resource_points = game_state.get_resources()
        accessible_resources = [
            rp
            for rp in resource_points
            if self.is_position_available(rp.get_position(), game_state)
        ]
        return min(
            accessible_resources, key=lambda rp: self.distance(unit, rp), default=None
        )

    def move_to_target(self, unit, target, game_state):
        """Moves a unit to a target position using MoveAction."""
        if unit.get_position() != target.get_position():
            if self.is_position_available(target.get_position(), game_state):
                action = MoveAction(game_state.get_map(), unit, target.get_position())
                game_state.add_action(action)

    def launch_attack(self, game_state):
        """Launches an attack on the nearest enemy target."""
        for unit in game_state.get_units(self):
            if isinstance(unit, (Swordsman, Archer, Horseman)):
                enemy = self.find_nearest_enemy(game_state, unit)
                if enemy:
                    self.move_to_target(unit, enemy, game_state)
                    if isinstance(enemy, type(unit)):
                        action = AttackUnitAction(unit, enemy)
                    else:
                        action = AttackBuildingAction(unit, enemy)
                    game_state.add_action(action)

    def needs_defense(self, game_state):
        """Checks if the AI needs to strengthen its defenses."""
        return (
            len(
                [
                    building
                    for building in game_state.get_buildings(self)
                    if isinstance(building, Keep)
                ]
            )
            < 2
        )

    def find_closest_resource(self, game_state, unit):
        """Finds the closest resource point for a villager to collect."""
        resource_points = game_state.get_resources()
        return min(
            resource_points, key=lambda rp: self.distance(unit, rp), default=None
        )

    def find_nearest_enemy(self, game_state, unit):
        """Finds the nearest enemy unit or building to attack."""
        enemies = game_state.get_units() | game_state.get_buildings()
        player_entities = game_state.get_units(self) | game_state.get_buildings(self)
        targets = enemies - player_entities
        return min(targets, key=lambda e: self.distance(unit, e), default=None)

    def distance(self, obj1, obj2):
        """Calculates the distance between two objects."""
        pos1, pos2 = obj1.get_position(), obj2.get_position()
        return (
            (pos1.get_x() - pos2.get_x()) ** 2 + (pos1.get_y() - pos2.get_y()) ** 2
        ) ** 0.5

    def has_resources_for(self, entity_type):
        """Checks if the AI has enough resources to train/build the specified entity."""
        cost = entity_type.get_cost()
        stock = self.get_resources()
        return (
            stock.get_wood() >= cost.get_wood()
            and stock.get_gold() >= cost.get_gold()
            and stock.get_food() >= cost.get_food()
        )

    def deduct_resources_for(self, entity_type):
        """Deducts the resources required for training/building the specified entity."""
        cost = entity_type.get_cost()
        stock = self.get_resources()
        stock.remove_wood(cost.get_wood())
        stock.remove_gold(cost.get_gold())
        stock.remove_food(cost.get_food())

    def get_resources(self):
        """Returns the current resource stock of the AI."""
        # Assuming the AI player object has a resource stock attribute
        return self.stock

