from core.actions.attack_building_action import AttackBuildingAction
from core.actions.move_action import MoveAction
from core.actions.move_and_track_action import MoveAndTrackAction
from core.actions.attack_unit_action import AttackUnitAction
from core.actions.attack_unit_by_building_action import AttackUnitByBuildingAction
from core.actions.build_action import BuildAction
from core.actions.collect_action import Collect_Action
from core.actions.training_action import TrainingAction
from core.actions.drop_off_action import DropOffAction
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
from core.buildings.camp import Camp
from core.units import Unit
from core.buildings import Building
from core.resources_points.wood import Wood
from core.resources_points.mine import Mine
from core.position import Position
from core.players import Player
import random

KEEPS_BY_BUILDINGS_DEFENSIVE = 1 / 4
KEEPS_BY_BUILDINGS_AGGRESSIVE = 1 / 6
VILLAGERS_BY_BUILDINGS = 1 / 1.5
ATTCKING_UNITS_TRAINERS_BY_BUILDINGS = 1 / 2
CAMPS_BY_BUILDINGS = 1 / 20


class AI(Player):
    def __init__(self, name, color, strategy="balanced"):
        super().__init__(name, color)
        # print(f"Initializing AI with name: {name} and strategy: {strategy}")
        self.name = name
        self.strategy = strategy  # Can be "defensive", "aggressive", or "balanced"
        self.failures = {"wood": 0, "gold": 0, "food": 0}

    def play(self, game_state):
        # print(f"AI {self.name} is playing with strategy: {self.strategy}")
        if self.strategy == "defensive":
            self.defensive_strategy(game_state)
        elif self.strategy == "aggressive":
            self.aggressive_strategy(game_state)
        elif self.strategy == "balanced":
            self.balanced_strategy(game_state)

    def always_executing_strategy(self, game_state):
        print(
            "Required villagers:",
            len(game_state.get_map().get_buildings(self))
            // (1 / VILLAGERS_BY_BUILDINGS),
        )
        print(
            "Current villagers:",
            len(
                [
                    u
                    for u in game_state.get_map().get_units(self)
                    if isinstance(u, Villager)
                ]
            ),
        )
        if len(
            [u for u in game_state.get_map().get_units(self) if isinstance(u, Villager)]
        ) <= len(game_state.get_map().get_buildings(self)) // (
            1 / VILLAGERS_BY_BUILDINGS
        ):
            for building in game_state.get_map().get_buildings(self):
                if isinstance(building, TownCenter):
                    print("Training villager")
                    self.train_unit(Villager, building, game_state)

        if self.needs_defense(game_state):
            print("Building keep")
            self.build_structure(Keep, game_state)

        self.build_camps(game_state)

        self.manage_economy(game_state)

        self.keeps_attack(game_state)

    def defensive_strategy(self, game_state):
        print(f"{self.name} is executing defensive strategy")
        self.divide_units_across_buildings(game_state)
        self.always_executing_strategy(game_state)

    def aggressive_strategy(self, game_state):
        for building in game_state.get_map().get_buildings(self):
            if not building.is_built():
                continue
            if isinstance(building, Barracks):
                self.train_unit(Swordsman, building, game_state)
            elif isinstance(building, ArcheryRange):
                self.train_unit(Archer, building, game_state)
            elif isinstance(building, Stable):
                self.train_unit(Horseman, building, game_state)

        if self.requires_aggressive_buildings(game_state):
            choices = [Barracks, ArcheryRange, Stable]
            self.build_structure(random.choice(choices), game_state)

        self.launch_attack(game_state)
        self.always_executing_strategy(game_state)

    def balanced_strategy(self, game_state):
        # print(f"{self.name} is executing balanced strategy")
        if self.needs_defense(game_state):
            self.defensive_strategy(game_state)
        else:
            self.aggressive_strategy(game_state)

    def build_camps(self, game_state):
        if len(
            [
                b
                for b in game_state.get_map().get_buildings(self)
                if isinstance(b, Camp) or isinstance(b, TownCenter)
            ]
        ) <= len(game_state.get_map().get_buildings(self)) // (1 / CAMPS_BY_BUILDINGS):
            self.build_structure(Camp, game_state)

    def keeps_attack(self, game_state):
        for building in game_state.get_map().get_buildings(self):
            if isinstance(building, Keep):
                attack_range = building.get_range()
                attack_damage = building.get_damage()
                attack_speed = building.get_attack_speed()
                my_objects = game_state.get_map().get_units(
                    self
                ) | game_state.get_map().get_buildings(self)
                all_objects = (
                    game_state.get_map().get_units()
                    | game_state.get_map().get_buildings()
                )
                enemies = all_objects - my_objects
                for enemy in enemies:
                    if self._safe_distance(building, enemy) <= attack_range:
                        action = AttackUnitByBuildingAction(building, enemy)
                        game_state.add_action(action)

    def divide_units_across_buildings(self, game_state):
        if len(game_state.get_map().get_buildings(self)) == 0:
            return
        # Get all player village zones (building tiles)
        player_village_zone = {
            Position(x, y)
            for building in game_state.get_map().get_buildings(self)
            for x in range(
                building.get_position().get_x(),
                building.get_position().get_x() + building.get_width(),
            )
            for y in range(
                building.get_position().get_y(),
                building.get_position().get_y() + building.get_height(),
            )
        }

        min_x = min([p.get_x() for p in player_village_zone])
        max_x = max([p.get_x() for p in player_village_zone])
        min_y = min([p.get_y() for p in player_village_zone])
        max_y = max([p.get_y() for p in player_village_zone])

        available_positions = set()
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.is_position_available(Position(x, y), game_state):
                    available_positions.add(Position(x, y))

        for unit in game_state.get_map().get_units(self):
            unit_x = unit.get_position().get_x()
            unit_y = unit.get_position().get_y()
            is_in_range = min_x <= unit_x <= max_x and min_y <= unit_y <= max_y
            if (
                isinstance(unit, Swordsman)
                or isinstance(unit, Horseman)
                or isinstance(unit, Archer)
            ) and not is_in_range:
                if (
                    not self.is_attacker_available(game_state, unit)
                    or len(available_positions) == 0
                ):
                    continue
                closest_position = min(
                    available_positions,
                    key=lambda p: self._safe_distance(unit, p),
                    default=None,
                )
                if closest_position:
                    action = MoveAction(game_state.get_map(), unit, closest_position)
                    game_state.add_action(action)
                    available_positions.remove(closest_position)

    def requires_aggressive_buildings(self, game_state):
        return sum(
            isinstance(building, Barracks)
            or isinstance(building, ArcheryRange)
            or isinstance(building, Stable)
            for building in game_state.get_map().get_buildings(self)
        ) <= len(game_state.get_map().get_buildings(self)) // (
            1 / ATTCKING_UNITS_TRAINERS_BY_BUILDINGS
        )

    def train_unit(self, unit_type, building, game_state):
        print(f"Training unit {unit_type.__name__} at building {building}")
        if building.is_training():
            return
        action = TrainingAction(game_state.get_map(), building, unit_type)
        if self.has_resources_for(unit_type):
            print(f"Sufficient resources for {unit_type.__name__}, adding action")
            game_state.add_action(action)
            self.deduct_resources_for(unit_type)
        else:
            print(f"Not enough resources for {unit_type.__name__}")

    def build_structure(self, structure_type, game_state):
        # print(f"Attempting to build structure {structure_type.__name__}")
        # print(f"Resources: {self.get_resources()}")
        # print(f"Available villagers: {self.count_available_villagers(game_state)}")
        if (
            self.has_resources_for(structure_type)
            and self.count_available_villagers(game_state) >= 1
        ):
            position = self.find_building_position(game_state, structure_type)
            if position:
                print(f"Found position {position} for {structure_type.__name__}")
                new_building = structure_type(position, self)
                game_state.get_map().add_building(new_building)
                self.deduct_resources_for(structure_type)
                build_action = BuildAction(new_building)
                game_state.add_action(build_action)

                for unit in game_state.get_map().get_units(self):
                    if isinstance(unit, Villager) and self.is_villager_available(
                        game_state, unit
                    ):
                        build_action.add_builder(unit)
                        # print(f"Assigned builder {unit} to {structure_type.__name__}")
                        # print("Distance:", self._safe_distance(unit, new_building))
                        if self._safe_distance(unit, new_building) > 4:
                            # print(f"Moving {unit} to {new_building.get_position()}")
                            closest_position = (
                                self.find_closest_position_arround_object(
                                    new_building, game_state
                                )
                            )
                            # print(f"Closest position: {closest_position}")
                            game_state.add_action(
                                MoveAction(game_state.get_map(), unit, closest_position)
                            )
                        if build_action.nb_builders >= 3:
                            break
            else:
                # pass
                print(f"No valid position found for {structure_type.__name__}")
        else:
            # pass
            print(
                f"Not enough resources for {structure_type.__name__} or no available builders"
            )

    def find_closest_position_arround_object(self, object, game_state):
        available_positions = set()
        for x in range(
            object.get_position().get_x() - 1,
            object.get_position().get_x()
            + (object.get_width() if isinstance(object, Building) else 1)
            + 1,
        ):
            for y in range(
                object.get_position().get_y() - 1,
                object.get_position().get_y()
                + (object.get_height() if isinstance(object, Building) else 1)
                + 1,
            ):
                if self.is_position_available(Position(x, y), game_state):
                    available_positions.add(Position(x, y))
        return random.choice(list(available_positions))

    def is_villager_available(self, game_state, villager):
        for action in game_state.get_actions():
            if (
                isinstance(action, TrainingAction)
                or isinstance(action, AttackBuildingAction)
                or isinstance(action, AttackUnitAction)
                or isinstance(action, AttackUnitByBuildingAction)
            ):
                continue
            for unit in action.get_involved_units():
                if unit == villager:
                    return False
        return True

    def count_available_villagers(self, game_state):
        used_villagers = set()
        for action in game_state.get_actions():
            if (
                isinstance(action, TrainingAction)
                or isinstance(action, AttackBuildingAction)
                or isinstance(action, AttackUnitAction)
                or isinstance(action, AttackUnitByBuildingAction)
            ):
                continue
            for unit in action.get_involved_units():
                if isinstance(unit, Villager) and unit.get_player() == self:
                    used_villagers.add(unit)
        return len(
            [u for u in game_state.get_map().get_units(self) if isinstance(u, Villager)]
        ) - len(used_villagers)

    def find_building_position(self, game_state, structure_type):
        # print(f"Finding position for {structure_type.__name__}")
        map_width = game_state.get_map().get_width()
        map_height = game_state.get_map().get_height()
        player_entities = game_state.get_map().get_buildings(
            self
        ) | game_state.get_map().get_units(self)
        # enemy_entities = (
        #     game_state.get_map().get_buildings()
        #     | game_state.get_map().get_units() - player_entities
        # )

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
                    # enemy_distance = sum(
                    #     self._safe_distance(position, e.get_position())
                    #     for e in enemy_entities
                    # )
                    # score = enemy_distance - player_distance
                    score = -player_distance
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

        for dx in range(-1, width + 1):
            for dy in range(-1, height + 1):
                x, y = position.get_x() + dx, position.get_y() + dy
                if x >= map_width or y >= map_height:
                    return False
                test_position = Position(x, y)
                if not self.is_position_available(
                    test_position, game_state, check_walkable=False
                ):
                    return False

        return True

    def manage_economy(self, game_state):
        # print(f"Managing economy for {self.name}")

        exec_order = ["process_houses", "process_farms", "process_resources"]
        random.shuffle(exec_order)
        for action in exec_order:
            getattr(self, action)(game_state)

    def process_houses(self, game_state):
        if self.needs_more_houses(game_state):
            self.build_structure(House, game_state)

    def process_farms(self, game_state):
        if self.needs_more_food(game_state):
            self.build_structure(Farm, game_state)

    def process_resources(self, game_state):
        self.collect_resources(game_state)
        self.drop_off_resources(game_state)

    def drop_off_resources(self, game_state):
        for unit in game_state.get_map().get_units(self):
            if (
                isinstance(unit, Villager)
                and sum(unit.get_stock().values()) >= 20
                and self.is_villager_available(game_state, unit)
            ):
                print("Dropping off resources for ", unit)
                for building in game_state.get_map().get_buildings(self):
                    if isinstance(building, TownCenter) or isinstance(building, Camp):
                        if self._safe_distance(unit, building) > 2:
                            closest_position = (
                                self.find_closest_position_arround_object(
                                    building, game_state
                                )
                            )
                            game_state.add_action(
                                MoveAction(game_state.get_map(), unit, closest_position)
                            )
                        drop_off_action = DropOffAction(unit, building)
                        game_state.add_action(drop_off_action)

    def needs_more_houses(self, game_state):
        current_population = len(game_state.get_map().get_units(self))
        max_population = game_state.get_map().calculate_max_number_units(self)
        result = current_population + 5 >= max_population
        # print(f"Needs more houses: {result}")
        return result

    def needs_more_food(self, game_state):
        # result = self.get_resources().get_food() < 50
        # check for all farms of player remaining food stock
        sum = 0
        for building in game_state.get_map().get_buildings(self):
            if isinstance(building, Farm):
                sum += building.get_resource().get_food()
        result = (sum + self.get_stock().get_food()) < 500
        # print(f"Needs more food: {result}")
        return result

    def collect_resources(self, game_state):
        # print(f"Collecting resources for {self.name}")
        for unit in game_state.get_map().get_units(self):
            if (
                isinstance(unit, Villager)
                and self.is_villager_available(game_state, unit)
                and sum(unit.get_stock().values()) < 20
            ):
                resource_point = self.find_closest_resource(
                    game_state, unit, self.get_resource_to_collect()
                )
                if resource_point:
                    self.move_to_collect(unit, resource_point, game_state)

    def move_to_collect(self, unit, resource_point, game_state):
        # print(f"Moving {unit} to collect from {resource_point}")
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

    def is_position_available(self, position, game_state, check_walkable=True):
        # make sure position is within map boundaries
        if (
            position.get_x() < 0
            or position.get_x() >= game_state.get_map().get_width()
            or position.get_y() < 0
            or position.get_y() >= game_state.get_map().get_height()
        ):
            return False
        for building in game_state.get_map().get_buildings():
            if (
                building.get_position().get_x()
                <= position.get_x()
                < building.get_position().get_x() + building.get_width()
                and building.get_position().get_y()
                <= position.get_y()
                < building.get_position().get_y() + building.get_height()
            ):
                if check_walkable:
                    return building.is_walkable()
                else:
                    return False
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

    def move_to_target(self, unit, target, game_state, track=False):
        target_position = self.find_farest_position_arround_object_within_unit_range(
            target, game_state, unit
        )
        if not target_position:
            return
        if unit.get_position() != target_position:
            if self.is_position_available(target_position, game_state):
                action = MoveAction(game_state.get_map(), unit, target_position)
                game_state.add_action(action)

    def find_farest_position_arround_object_within_unit_range(
        self, object, game_state, unit
    ):
        unit_range = int(unit.get_range())
        # print(unit_range)
        # find valid positions (must be dx**2 + dy**2 <= unit_range) but choose the farest
        best_position = None
        best_distance = 0
        # print(f"Finding farest position for {unit} around {object}")
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                # print(f"Checking position {dx}, {dy}")
                x, y = (
                    object.get_position().get_x() + dx,
                    object.get_position().get_y() + dy,
                )
                # print(f"Checking position {x}, {y}")
                test_position = Position(x, y)
                if self._safe_distance(test_position, object) > unit_range:
                    continue
                # print("is_position_available", self.is_position_available(test_position, game_state))
                if self.is_position_available(test_position, game_state):
                    # print("safe_distance", self._safe_distance(unit, test_position))
                    distance = self._safe_distance(unit, test_position)
                    if distance > best_distance:
                        best_distance = distance
                        best_position = test_position
        # print(f"Best position: {best_position}")
        return best_position

    def launch_attack(self, game_state):
        print(f"Launching attack for {self.name}")
        for unit in game_state.get_map().get_units(self):
            if not self.is_attacker_available(game_state, unit):
                continue
            if isinstance(unit, (Swordsman, Archer, Horseman)):
                enemy = self.find_nearest_enemy(game_state, unit)
                if enemy:
                    if isinstance(enemy, Unit):
                        move_and_track_action = MoveAndTrackAction(
                            game_state.get_map(), unit, enemy
                        )
                        game_state.add_action(move_and_track_action)
                        action = AttackUnitAction(unit, enemy)
                        game_state.add_action(action)
                    else:
                        self.move_to_target(unit, enemy, game_state)
                        action = AttackBuildingAction(unit, enemy)
                        game_state.add_action(action)

    def is_attacker_available(self, game_state, attacker):
        for action in game_state.get_actions():
            if isinstance(action, AttackUnitAction) or isinstance(
                action, AttackBuildingAction
            ):
                if action.get_attacking_unit() == attacker:
                    return False
            if isinstance(action, MoveAndTrackAction) or isinstance(action, MoveAction):
                if action.get_unit() == attacker:
                    return False
        return True

    def needs_defense(self, game_state):
        result = len(
            [
                building
                for building in game_state.get_map().get_buildings(self)
                if isinstance(building, Keep)
            ]
        ) <= len(game_state.get_map().get_buildings(self)) // (
            1
            / (
                KEEPS_BY_BUILDINGS_DEFENSIVE
                if self.strategy == "defensive"
                else KEEPS_BY_BUILDINGS_AGGRESSIVE
            )
        )
        print(f"Needs defense: {result}")
        return result

    def find_closest_resource(self, game_state, unit, target_resource=None):
        table = {"wood": Wood, "gold": Mine, "food": Farm}
        resource_points = (
            game_state.get_map()
            .get_resources()
            .union(
                set(
                    [
                        b
                        for b in game_state.get_map().get_buildings(self)
                        if isinstance(b, Farm)
                    ]
                )
            )
        )
        target_resource_point = table[target_resource] if target_resource else None
        if target_resource_point:
            resource_points = [
                rp for rp in resource_points if isinstance(rp, target_resource_point)
            ]
        # self.failures[target_resource] = 0
        return min(
            resource_points, key=lambda rp: self._safe_distance(unit, rp), default=None
        )

    def find_nearest_enemy(self, game_state, unit):
        enemies = (
            game_state.get_map().get_units()
            | game_state.get_map().get_buildings()
            # game_state.get_map().get_buildings()
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
        dist = (pos1.get_x() - pos2.get_x()) ** 2 + (pos1.get_y() - pos2.get_y()) ** 2
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
        # failures count
        # if not result:
        #     self.failures["wood"] += cost.get_wood() / (stock.get_wood() or 1)
        #     self.failures["gold"] += cost.get_gold() / (stock.get_gold() or 1)
        #     self.failures["food"] += cost.get_food() / (stock.get_food() or 1)
        # print(f"Failures: {self.failures}")
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
