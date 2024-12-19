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


class MyTriangle:
    def __init__(self, v1=None, v2=None, v3=None, x1=None, y1=None, x2=None, y2=None, x3=None, y3=None):
        if v1 is not None and v2 is not None and v3 is not None:
            self.v1 = v1
            self.v2 = v2
            self.v3 = v3
        else:
            self.v1 = MyPoint(x1, y1)
            self.v2 = MyPoint(x2, y2)
            self.v3 = MyPoint(x3, y3)

    def get_v1(self):
        return self.v1

    def set_v1(self, v1):
        self.v1 = v1

    def get_v2(self):
        return self.v2

    def set_v2(self, v2):
        self.v2 = v2

    def get_v3(self):
        return self.v3

    def set_v3(self, v3):
        self.v3 = v3

    def get_perimeter(self):
        return self.v1.distance(another=self.v2) + self.v2.distance(another=self.v3) + self.v3.distance(another=self.v1)

    def get_type(self):
        d1 = self.v1.distance(another=self.v2)
        d2 = self.v2.distance(another=self.v3)
        d3 = self.v3.distance(another=self.v1)
        if d1 == d2 == d3:
            return "Equilateral"
        elif d1 == d2 or d2 == d3 or d1 == d3:
            return "Isosceles"
        else:
            return "Scalene"

    def __str__(self):
        return f"MyTriangle[v1={self.v1},v2={self.v2},v3={self.v3}]"


if __name__ == "__main__":
    triangle3 = MyTriangle(MyPoint(1, 1), MyPoint(2, 2), MyPoint(3, 3))
    print(triangle3.get_perimeter())
    print(triangle3.get_type())