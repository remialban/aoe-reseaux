from core.actions.attack_building_action import AttackBuildingAction
from core.actions.move_action import MoveAction
from core.actions.attack_unit_action import AttackUnitAction
from core.actions.build_action import BuildAction
from core.actions.collect_action import Collect_Action
from core.actions.training_action import TrainingAction
from core.units.villager import Villager
from core.units.archer import Archer
from core.units.horse_man import Horseman
from core.units.swordsman import Swordsman
from core.buildings.town_center import TownCenter
from core.buildings.barracks import Barracks
from core.buildings.archery_range import ArcheryRange
from core.buildings.stable import Stable
from core.buildings.house import House
from core.buildings.farm import Farm
from core.buildings.keep import Keep
from core.position import Position
from core.players import Player


class AI(Player):
    def __init__(self, name, color, strategy="balanced"):
        super().__init__(name, color)
        # print(f"Initializing AI with name: {name} and strategy: {strategy}")
        self.name = name
        self.strategy = strategy  # Can be "defensive", "aggressive", or "balanced"

    def play(self, game_state):
        # print(f"AI {self.name} is playing with strategy: {self.strategy}")
        if self.strategy == "defensive":
            self.defensive_strategy(game_state)
        elif self.strategy == "aggressive":
            self.aggressive_strategy(game_state)
        elif self.strategy == "balanced":
            self.balanced_strategy(game_state)

    def defensive_strategy(self, game_state):
        # print(f"{self.name} is executing defensive strategy")
        for building in game_state.get_map().get_buildings(self):
            if isinstance(building, TownCenter):
                self.train_unit(Villager, building, game_state)

        if self.needs_defense(game_state):
            self.build_structure(Keep, game_state)

        self.manage_economy(game_state)

    def aggressive_strategy(self, game_state):
        # print(f"{self.name} is executing aggressive strategy")
        for building in game_state.get_map().get_buildings(self):
            if isinstance(building, Barracks):
                self.train_unit(Swordsman, building, game_state)
            elif isinstance(building, ArcheryRange):
                self.train_unit(Archer, building, game_state)
            elif isinstance(building, Stable):
                self.train_unit(Horseman, building, game_state)

        self.launch_attack(game_state)
        self.manage_economy(game_state)

    def balanced_strategy(self, game_state):
        # print(f"{self.name} is executing balanced strategy")
        if self.needs_defense(game_state):
            self.defensive_strategy(game_state)
        else:
            self.aggressive_strategy(game_state)

    def train_unit(self, unit_type, building, game_state):
        # print(f"Training unit {unit_type.__name__} at building {building}")
        action = TrainingAction(game_state.get_map(), building, unit_type)
        if self.has_resources_for(unit_type):
            # print(f"Sufficient resources for {unit_type.__name__}, adding action")
            game_state.add_action(action)
            self.deduct_resources_for(unit_type)
        else:
            pass
            # print(f"Not enough resources for {unit_type.__name__}")

    def build_structure(self, structure_type, game_state):
        # print(f"Attempting to build structure {structure_type.__name__}")
        if self.has_resources_for(structure_type):
            position = self.find_building_position(game_state, structure_type)
            if position:
                print(f"Found position {position} for {structure_type.__name__}")
                new_building = structure_type(position, self)
                self.deduct_resources_for(structure_type)
                build_action = BuildAction(new_building)
                game_state.add_action(build_action)

                for unit in game_state.get_map().get_units(self):
                    if isinstance(unit, Villager):
                        build_action.add_builder(unit)
                        print(f"Assigned builder {unit} to {structure_type.__name__}")
                        if build_action.nb_builders >= 3:
                            break
            else:
                print(f"No valid position found for {structure_type.__name__}")
        else:
            print(f"Not enough resources for {structure_type.__name__}")

    def find_building_position(self, game_state, structure_type):
        # print(f"Finding position for {structure_type.__name__}")
        map_width = game_state.get_map().get_width()
        map_height = game_state.get_map().get_height()
        player_entities = game_state.get_map().get_buildings(
            self
        ) | game_state.get_map().get_units(self)
        enemy_entities = (
            game_state.get_map().get_buildings()
            | game_state.get_map().get_units() - player_entities
        )

        best_position = None
        best_score = float("-inf")

        for x in range(map_width):
            for y in range(map_height):
                position = Position(x, y)
                if self.is_area_available(position, structure_type, game_state):
                    player_distance = sum(
                        self._safe_distance(position, e.get_position())
                        for e in player_entities
                    )
                    enemy_distance = sum(
                        self._safe_distance(position, e.get_position())
                        for e in enemy_entities
                    )
                    score = enemy_distance - player_distance
                    if score > best_score:
                        best_score = score
                        best_position = position

        # print(f"Best position for {structure_type.__name__}: {best_position}")
        return best_position

    def _safe_distance(self, pos1, pos2):
        """Helper function to safely calculate distance."""
        distance = self.distance(pos1, pos2)
        if isinstance(distance, complex):
            # Handle complex numbers by using the magnitude or real part
            return abs(distance)  # Use magnitude of the complex number
        return distance

    def is_area_available(self, position, structure_type, game_state):
        width, height = (
            structure_type(Position(0, 0), Player("", "")).get_width(),
            structure_type(Position(0, 0), Player("", "")).get_height(),
        )
        map_width = game_state.get_map().get_width()
        map_height = game_state.get_map().get_height()

        for dx in range(width):
            for dy in range(height):
                x, y = position.get_x() + dx, position.get_y() + dy
                if x >= map_width or y >= map_height:
                    return False
                test_position = Position(x, y)
                if not self.is_position_available(test_position, game_state):
                    return False

        return True

    def manage_economy(self, game_state):
        # print(f"Managing economy for {self.name}")
        if self.needs_more_houses(game_state):
            self.build_structure(House, game_state)

        if self.needs_more_food(game_state):
            self.build_structure(Farm, game_state)

        self.collect_resources(game_state)

    def needs_more_houses(self, game_state):
        current_population = len(game_state.get_map().get_units(self))
        max_population = game_state.get_map().calculate_max_number_units(self)
        result = current_population + 5 >= max_population
        # print(f"Needs more houses: {result}")
        return result

    def needs_more_food(self, game_state):
        result = self.get_resources().get_food() < 50
        # print(f"Needs more food: {result}")
        return result

    def collect_resources(self, game_state):
        # print(f"Collecting resources for {self.name}")
        for unit in game_state.get_map().get_units(self):
            if isinstance(unit, Villager):
                resource_point = self.find_closest_resource(game_state, unit)
                if resource_point:
                    self.move_to_collect(unit, resource_point, game_state)

    def move_to_collect(self, unit, resource_point, game_state):
        print(f"Moving {unit} to collect from {resource_point}")
        if not self.is_position_available(resource_point.get_position(), game_state):
            alternative_resource = self.find_alternative_resource(game_state, unit)
            if alternative_resource:
                resource_point = alternative_resource

        if unit.get_position() != resource_point.get_position():
            move_action = MoveAction(
                game_state.get_map(), unit, resource_point.get_position()
            )
            game_state.add_action(move_action)

        collect_action = Collect_Action(unit, resource_point)
        game_state.add_action(collect_action)

    def is_position_available(self, position, game_state):
        for building in game_state.get_map().get_buildings():
            if building.get_position() == position:
                return building.is_walkable()
        for unit in game_state.get_map().get_units():
            if unit.get_position() == position:
                return False
        return True

    def find_alternative_resource(self, game_state, unit):
        resource_points = game_state.get_map().get_resources()
        accessible_resources = [
            rp
            for rp in resource_points
            if self.is_position_available(rp.get_position(), game_state)
        ]
        return min(
            accessible_resources,
            key=lambda rp: self._safe_distance(unit, rp),
            default=None,
        )

    def move_to_target(self, unit, target, game_state):
        if unit.get_position() != target.get_position():
            if self.is_position_available(target.get_position(), game_state):
                action = MoveAction(game_state.get_map(), unit, target.get_position())
                game_state.add_action(action)

    def launch_attack(self, game_state):
        # print(f"Launching attack for {self.name}")
        for unit in game_state.get_map().get_units(self):
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
        result = (
            len(
                [
                    building
                    for building in game_state.get_map().get_buildings(self)
                    if isinstance(building, Keep)
                ]
            )
            < 2
        )
        # print(f"Needs defense: {result}")
        return result

    def find_closest_resource(self, game_state, unit):
        resource_points = game_state.get_map().get_resources()
        return min(
            resource_points, key=lambda rp: self._safe_distance(unit, rp), default=None
        )

    def find_nearest_enemy(self, game_state, unit):
        enemies = (
            game_state.get_map().get_units() | game_state.get_map().get_buildings()
        )
        player_entities = game_state.get_map().get_units(
            self
        ) | game_state.get_map().get_buildings(self)
        targets = enemies - player_entities
        return min(targets, key=lambda e: self._safe_distance(unit, e), default=None)

    def distance(self, obj1, obj2):
        pos1, pos2 = obj1.get_position() if not isinstance(obj1, Position) else obj1, (
            obj2.get_position() if not isinstance(obj2, Position) else obj2
        )
        dist = (pos1.get_x() - pos2.get_x()) ** 2 + (pos1.get_y() - pos2.get_y()) ** 0.5
        # print(f"Distance between {obj1} and {obj2}: {dist}")
        return dist

    def has_resources_for(self, entity_type):
        cost = entity_type(Player("", ""), Position(0, 0)).get_cost_resource()
        stock = self.get_resources()
        result = (
            stock.get_wood() >= cost.get_wood()
            and stock.get_gold() >= cost.get_gold()
            and stock.get_food() >= cost.get_food()
        )
        # print(f"Has resources for {entity_type.__name__}: {result}")
        return result

    def deduct_resources_for(self, entity_type):
        cost = entity_type(Player("", ""), Position(0, 0)).get_cost_resource()
        stock = self.get_resources()
        # print(f"Deducting resources for {entity_type.__name__}: {cost}")
        stock.remove_wood(cost.get_wood())
        stock.remove_gold(cost.get_gold())
        stock.remove_food(cost.get_food())

    def get_resources(self):
        # print(f"Fetching resources for {self.name}")
        return self.stock
