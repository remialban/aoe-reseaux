from core.players import Player
from core.units.villager import Villager
from core.units.archer import Archer
from core.units.swordsman import Swordsman
from core.units.horse_man import Horseman
from core.actions.collect_action import Collect_Action
from core.actions.move_action import MoveAction
from core.actions.attack_unit_action import AttackUnitAction
from core.actions.attack_building_action import AttackBuildingAction
from core.map import Map
from core.buildings import Building, Barracks, Stable, ArcheryRange
from core.resources_points import ResourcePoint
from core.position import Position


class AI(Player):
    def __init__(self, name, color, resource):
        super().__init__(name, color, resource)

    def play(self, game_map: Map):
        """
        Perform all possible actions for the AI player during a turn.
        """
        units = game_map.get_units(self)
        buildings = game_map.get_buildings(self)
        resources = game_map.get_resources()

        self.gather_resources(units, resources)
        self.build_structures(game_map)
        self.train_units(buildings)
        self.attack_enemies(units, game_map)

    def gather_resources(self, units, resources):
        """Assign villagers to gather resources."""
        for unit in units:
            if isinstance(unit, Villager):
                nearest_resource = self.find_nearest_resource(unit, resources)
                if nearest_resource:
                    collect_action = Collect_Action(unit, nearest_resource)
                    collect_action.do_action_collect()

    def build_structures(self, game_map):
        """Build new structures if resources allow."""
        if self.has_enough_resources({"wood": 50}):
            position = self.find_empty_position(game_map)
            if position:
                self.subtract_resources({"wood": 50})
                self.add_building(Barracks(position))

    def train_units(self, buildings):
        """Train units if resources allow."""
        for building in buildings:
            if isinstance(building, (Barracks, Stable, ArcheryRange)):
                if self.has_enough_resources({"food": 50, "gold": 20}):
                    self.subtract_resources({"food": 50, "gold": 20})
                    self.add_unit(Swordsman(building.get_position()))

    def attack_enemies(self, units, game_map):
        """Command units to attack enemies."""
        for unit in units:
            if isinstance(unit, (Archer, Swordsman, Horseman)):
                target = self.find_nearest_enemy(unit, game_map)
                if target:
                    self.perform_attack(unit, target)

    def perform_attack(self, unit, target):
        """Execute an attack action."""
        if isinstance(target, Building):
            attack_action = AttackBuildingAction(unit, target)
        else:
            attack_action = AttackUnitAction(unit, target)
        attack_action.do_action()

    def find_nearest_resource(self, unit, resources):
        """Find the nearest resource point to the unit."""
        unit_position = unit.get_position()
        return min(
            resources,
            key=lambda res: unit_position.get_distance(res.get_position()),
            default=None,
        )

    def find_nearest_enemy(self, unit, game_map):
        """Find the nearest enemy unit or building."""
        unit_position = unit.get_position()
        enemies = game_map.get_units() + game_map.get_buildings()
        enemies = [e for e in enemies if e.get_player() != self]
        return min(
            enemies,
            key=lambda e: unit_position.get_distance(e.get_position()),
            default=None,
        )

    def find_empty_position(self, game_map):
        """Find an empty position for building."""
        for x in range(game_map.get_width()):
            for y in range(game_map.get_height()):
                position = Position(x, y)
                if not game_map.is_position_occupied(position):
                    return position
        return None

    def has_enough_resources(self, cost):
        """Check if resources meet the required cost."""
        return all(
            getattr(self.stock, f"get_{res}")() >= amount
            for res, amount in cost.items()
        )

    def subtract_resources(self, cost):
        """Deduct resources used for an action."""
        for res, amount in cost.items():
            getattr(self.stock, f"add_{res}")(-amount)

    def add_building(self, building):
        """Add a building to the player's control."""
        self.buildings.append(building)

    def add_unit(self, unit):
        """Add a unit to the player's control."""
        self.units.append(unit)
