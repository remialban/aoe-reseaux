from math import radians, cos, sin

class Isometry:
    """
    Function to convert x, y coordinates to isometric coordinates
    """
    def __init__(self, tile_length):
        """
        :param tile_length: length of a tile
        """
        self.tile_length = tile_length

    def get_tile_length(self):
        if callable(self.tile_length):
            return self.tile_length()
        return self.tile_length

    def x_to_iso(self, x, y, offset_x):
        """
        Apply the x offset to the x coordinate
        :param x: x coordinate
        :param y: y coordinate
        :param offset_x: x offset
        :return:
        """
        angle = radians(30)
        offset_x *= self.get_tile_length()
        new_x = cos(angle) * offset_x
        new_y = sin(angle) * offset_x

        return new_x + x, new_y + y

    def y_to_iso(self, x, y, offset_y):
        angle = radians(30)
        offset_y *= self.get_tile_length()
        new_x = - cos(angle) * offset_y
        new_y = sin(angle) * offset_y

        return new_x + x, new_y + y

    def x_y_to_iso(self, x, y):
        new_x, new_y = self.x_to_iso(0, 0, x,)
        new_x, new_y = self.y_to_iso(new_x, new_y, y)

        return new_x, new_y
