for b in self.buildings:

    list_positions: set[tuple[int]]= set()

    for i in range(b.get_height()):
        for j in range(b.get_width()):
            list_positions.add((b.get_position().get_x() + i, b.get_position().get_y() + j))

    for i in range(building.get_width()):
        for j in range(building.get_width()):
            if (building.get_position().get_x() + i, building.get_position().get_y() + j) in list_positions:
                return False

    return True
