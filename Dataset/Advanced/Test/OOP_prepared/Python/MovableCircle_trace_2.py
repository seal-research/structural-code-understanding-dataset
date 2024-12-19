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


class MovableCircle(Movable):
    def __init__(self, radius=0, center=None, x=0, y=0, x_speed=0, y_speed=0):
        self.radius = radius
        if center is None:
            self.center = MovablePoint(x, y, x_speed, y_speed)
        else:
            self.center = center

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center

    def __str__(self):
        return f"{self.center}, radius={self.radius}"

    def move_up(self):
        self.center.set_y(self.center.get_y() - self.center.get_y_speed())

    def move_down(self):
        self.center.set_y(self.center.get_y() + self.center.get_y_speed())

    def move_left(self):
        self.center.set_x(self.center.get_x() - self.center.get_x_speed())

    def move_right(self):
        self.center.set_x(self.center.get_x() + self.center.get_x_speed())


if __name__ == "__main__":
    m2 = MovableCircle(radius=10, x=15, y=15, x_speed=4, y_speed=4)
    print(m2)
    m2.move_up()
    print(m2)