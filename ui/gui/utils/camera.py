class Camera:
    coors = [0, 0]
    tile_length = 50

    @staticmethod
    def zoom_in():
        Camera.tile_length *= 1.1

    @staticmethod
    def zoom_out():
        Camera.tile_length *= 0.9

    @staticmethod
    def get_tile_length():
        return Camera.tile_length

    @staticmethod
    def get_x():
        return Camera.coors[0]

    @staticmethod
    def get_y():
        return Camera.coors[1]

    @staticmethod
    def apply_offset(x, y):
        return x - Camera.coors[0], y - Camera.coors[1]

    @staticmethod
    def add_x(value):
        Camera.coors = (Camera.coors[0] + value, Camera.coors[1])

    @staticmethod
    def add_y(value):
        Camera.coors = (Camera.coors[0], Camera.coors[1] + value)

    @staticmethod
    def set_camera(x, y):
        Camera.coors = (x, y)