from core.actions import Action
from core.units import Unit
from core.position import Position
from core.buildings import Building
from core.map import Map
import heapq
from typing import List, Set


class MoveAndTrackAction(Action):
    __new_position: Position
    __buildings: Set[Building]
    __path: List[Position]
    __current_step: int
    __map_width: int
    __map_height: int

    def __init__(self, map: Map, unit: Unit, target_unit: Unit):
        self.__buildings = map.buildings
        self.__map_width = map.get_width()
        self.__map_height = map.get_height()
        self.set_involved_units(set([unit]))
        self.__target_unit = target_unit
        self.__latest_position = target_unit.get_position()
        self.__new_position = (
            self.find_farest_position_arround_object_within_unit_range(
                target_unit, unit
            )
        )

        self.__path = self._find_path()

        self.__current_step = 0
        super().__init__()

    def get_unit(self):
        return next(iter(self.get_involved_units()))

    def get_target_unit(self):
        return self.__target_unit

    def do_action(self) -> bool:
        self.before_action()

        if self.__target_unit.get_position() != self.__latest_position:
            self.__latest_position = self.__target_unit.get_position()
            self.__path = self._find_path()
            self.__current_step = 0
            self.__new_position = (
                self.find_farest_position_arround_object_within_unit_range(
                    self.__target_unit, next(iter(self.get_involved_units()))
                )
            )

        if (
            self.__target_unit.get_health_points() <= 0
            or next(iter(self.get_involved_units())).get_health_points() <= 0
        ):
            return True

        if not self.__path:
            # print("No path found. Action cannot be performed.")
            return False

        time_per_step = 1 / (
            next(iter(self.get_involved_units())).get_movement_speed()
        )
        elapsed_time = (self.get_new_time() - self.get_old_time()).total_seconds()

        # print(f"Elapsed time: {elapsed_time}, Time per step: {time_per_step}")

        if elapsed_time >= time_per_step:
            self.__current_step += 1

            if self.__current_step >= len(self.__path):
                # print("Unit has reached the destination.")
                next(iter(self.get_involved_units())).change_position(
                    self.__new_position
                )
                return True

            else:
                next_position = self.__path[self.__current_step]
                # print(f"Moving to next position: {next_position}")
                next(iter(self.get_involved_units())).change_position(next_position)
                self.after_action()

        return False

    def _find_path(self) -> List[Position]:
        start = next(iter(self.get_involved_units())).get_position()
        goal = self.__new_position

        # print(f"Finding path from {start} to {goal}")

        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            # print(f"Current position in pathfinding: {current}")

            if current == goal:
                # print("Goal reached during pathfinding.")
                return self._reconstruct_path(came_from, current)

            for neighbor in self._get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self._heuristic(
                        neighbor, goal
                    )
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    # print(f"Neighbor {neighbor} added to open set with f_score {f_score[neighbor]}")

        # print("Pathfinding failed. No valid path found.")
        return None

    def _heuristic(self, a: Position, b: Position):
        heuristic_value = abs(a.get_x() - b.get_x()) + abs(a.get_y() - b.get_y())
        # print(f"Heuristic from {a} to {b}: {heuristic_value}")
        return heuristic_value

    def _get_neighbors(self, position: Position):
        neighbors = []

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = position.get_x() + dx
            new_y = position.get_y() + dy

            if 0 <= new_x < self.__map_width and 0 <= new_y < self.__map_height:
                new_pos = Position(new_x, new_y)

                if self._is_valid_position(new_pos):
                    neighbors.append(new_pos)
                    # print(f"Valid neighbor found: {new_pos}")

        return neighbors

    def _is_valid_position(self, position: Position) -> bool:
        if not (
            0 <= position.get_x() < self.__map_width
            and 0 <= position.get_y() < self.__map_height
        ):
            # print(f"Position {position} is out of map bounds.")
            return False

        for building in self.__buildings:
            if not building.is_walkable():
                if (
                    building.get_position().get_x()
                    <= position.get_x()
                    < building.get_position().get_x() + building.get_width()
                    and building.get_position().get_y()
                    <= position.get_y()
                    < building.get_position().get_y() + building.get_height()
                ):
                    # print(f"Position {position} collides with building at {building.get_position()}.")
                    return False

        # print(f"Position {position} is valid.")
        return True

    def _reconstruct_path(self, came_from, current) -> List[Position]:
        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        reconstructed_path = path[::-1]
        # print(f"Reconstructed path: {reconstructed_path}")

        return reconstructed_path

    def find_farest_position_arround_object_within_unit_range(self, object, unit):
        unit_range = int(unit.get_range())
        best_position = None
        best_distance = 0
        for dx in range(-unit_range, unit_range + 1):
            for dy in range(-unit_range, unit_range + 1):
                if dx ** 2 + dy ** 2 > unit_range:
                    continue
                x, y = (
                    object.get_position().get_x() + dx,
                    object.get_position().get_y() + dy,
                )
                test_position = Position(x, y)
                if self._is_valid_position(test_position):
                    distance = self._safe_distance(unit, test_position)
                    if distance > best_distance:
                        best_distance = distance
                        best_position = test_position
        return best_position

    def distance(self, obj1, obj2):
        pos1, pos2 = obj1.get_position() if not isinstance(obj1, Position) else obj1, (
            obj2.get_position() if not isinstance(obj2, Position) else obj2
        )
        dist = (pos1.get_x() - pos2.get_x()) ** 2 + (pos1.get_y() - pos2.get_y()) ** 2
        # print(f"Distance between {obj1} and {obj2}: {dist}")
        return dist

    def _safe_distance(self, pos1, pos2):
        """Helper function to safely calculate distance."""
        distance = self.distance(pos1, pos2)
        if isinstance(distance, complex):
            # Handle complex numbers by using the magnitude or real part
            return abs(distance)  # Use magnitude of the complex number
        return distance


    def get_list_attributes(self):
        l = []
        for u in self.set_involved_units() :
            l.append([u.id,"position"])
        return l
