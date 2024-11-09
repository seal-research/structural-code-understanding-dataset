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

if __name__ == "__main__":
    p1 = MyPoint(2, 3)
    p2 = MyPoint(5, 7)
    print(p2.distance(another=p1))