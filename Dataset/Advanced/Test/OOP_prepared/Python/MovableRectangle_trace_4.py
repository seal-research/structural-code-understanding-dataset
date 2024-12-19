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
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_x_speed(self):
        return self.x_speed

    def set_x_speed(self, x_speed):
        self.x_speed = x_speed

    def get_y_speed(self):
        return self.y_speed

    def set_y_speed(self, y_speed):
        self.y_speed = y_speed

    def __str__(self):
        return f"({self.x},{self.y}) speed={self.x_speed},{self.y_speed}"

    def move_up(self):
        self.y -= self.y_speed

    def move_down(self):
        self.y += self.y_speed

    def move_left(self):
        self.x -= self.x_speed

    def move_right(self):
        self.x += self.x_speed


class MovableRectangle(Movable):
    def __init__(self, top_left=None, bottom_right=None):
        self.top_left = top_left if top_left else MovablePoint()
        self.bottom_right = bottom_right if bottom_right else MovablePoint()

    def get_top_left(self):
        return self.top_left

    def set_top_left(self, top_left):
        self.top_left = top_left

    def get_bottom_right(self):
        return self.bottom_right

    def set_bottom_right(self, bottom_right):
        self.bottom_right = bottom_right

    def __str__(self):
        return f"MovableRectangle[topLeft={self.top_left}, bottomRight={self.bottom_right}]"

    def move_up(self):
        self.top_left.set_y(self.top_left.get_y() - self.top_left.get_y_speed())
        self.bottom_right.set_y(self.bottom_right.get_y() - self.bottom_right.get_y_speed())

    def move_down(self):
        self.top_left.set_y(self.top_left.get_y() + self.top_left.get_y_speed())
        self.bottom_right.set_y(self.bottom_right.get_y() + self.bottom_right.get_y_speed())

    def move_left(self):
        self.top_left.set_x(self.top_left.get_x() - self.top_left.get_x_speed())
        self.bottom_right.set_x(self.bottom_right.get_x() - self.bottom_right.get_x_speed())

    def move_right(self):
        self.top_left.set_x(self.top_left.get_x() + self.top_left.get_x_speed())
        self.bottom_right.set_x(self.bottom_right.get_x() + self.bottom_right.get_x_speed())



if __name__ == "__main__":
    rectangle2 = MovableRectangle(MovablePoint(0, 0, 2, 2), MovablePoint(5, 5, 2, 2))
    rectangle2.move_left()
    rectangle2.move_down()
    print(rectangle2)