from abc import ABC, abstractmethod

class Movable(ABC):
    @abstractmethod
    def move_up(self):
        pass

    @abstractmethod
    def move_down(self):
        pass

    @abstractmethod
    def move_left(self):
        pass

    @abstractmethod
    def move_right(self):
        pass

class MovablePoint(Movable):
    def __init__(self, x=0, y=0, x_speed=0, y_speed=0):
        self._x = x
        self._y = y
        self._x_speed = x_speed
        self._y_speed = y_speed

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def x_speed(self):
        return self._x_speed

    @x_speed.setter
    def x_speed(self, value):
        self._x_speed = value

    @property
    def y_speed(self):
        return self._y_speed

    @y_speed.setter
    def y_speed(self, value):
        self._y_speed = value

    def __str__(self):
        return f"({self._x},{self._y}) speed={self._x_speed},{self._y_speed}"

    def move_up(self):
        self._y -= self._y_speed

    def move_down(self):
        self._y += self._y_speed

    def move_left(self):
        self._x -= self._x_speed

    def move_right(self):
        self._x += self._x_speed

if __name__ == "__main__":
    point = MovablePoint(5, 5, 2, 3)
    point.move_up()
    print(point)