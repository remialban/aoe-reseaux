class Position:
    __x: float
    __y: float

    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def set_x(self, x: float) -> None:
        self.__x = x

    def set_y(self, y: float) -> None:
        self.__y = y

    def __lt__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return (self.__x, self.__y) < (other.__x, other.__y)

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self.__x == other.__x and self.__y == other.__y

    def __hash__(self):
        return hash((self.__x, self.__y))

    def __str__(self):
        return f"({self.__x}, {self.__y})"

    def __repr__(self):
        return f"({self.__x}, {self.__y})"
