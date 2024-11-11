import math

class MyPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_xy(self):
        return [self.x, self.y]

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def distance(self, x=None, y=None, another=None):
        if another is not None:
            return math.sqrt((another.x - self.x) ** 2 + (another.y - self.y) ** 2)
        elif x is not None and y is not None:
            return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        else:
            return math.sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return f"({self.x},{self.y})"


class MyCircle:
    def __init__(self, center=None, radius=1):
        if isinstance(center, MyPoint):
            self.center = center
        elif isinstance(center, (list, tuple)) and len(center) == 2:
            self.center = MyPoint(center[0], center[1])
        else:
            self.center = MyPoint()
        self.radius = radius

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def get_center_x(self):
        return self.center.get_x()

    def get_center_y(self):
        return self.center.get_y()

    def set_center_x(self, x):
        self.center.set_x(x)

    def set_center_y(self, y):
        self.center.set_y(y)

    def get_center_xy(self):
        return self.center.get_xy()

    def set_center_xy(self, x, y):
        self.center.set_xy(x, y)

    def get_area(self):
        return math.pi * self.radius ** 2

    def get_circumference(self):
        return 2 * math.pi * self.radius

    def distance(self, another):
        return self.center.distance(another.center)

    def __str__(self):
        return f"MyCircle[radius={self.radius},center={self.center}]"


if __name__ == "__main__":
    my_circle = MyCircle(MyPoint(1, 1), 3)
    print(my_circle.distance(MyCircle(MyPoint(4, 5), 2)))