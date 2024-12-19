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
            return math.sqrt((0 - self.x) ** 2 + (0 - self.y) ** 2)

    def __str__(self):
        return f"({self.x},{self.y})"


class MyRectangle:
    def __init__(self, top_left=None, bottom_right=None, x1=None, y1=None, x2=None, y2=None):
        if top_left is not None and bottom_right is not None:
            self.top_left = top_left
            self.bottom_right = bottom_right
        elif x1 is not None and y1 is not None and x2 is not None and y2 is not None:
            self.top_left = MyPoint(x1, y1)
            self.bottom_right = MyPoint(x2, y2)
        else:
            self.top_left = MyPoint()
            self.bottom_right = MyPoint()

    def get_top_left(self):
        return self.top_left

    def set_top_left(self, top_left):
        self.top_left = top_left

    def get_bottom_right(self):
        return self.bottom_right

    def set_bottom_right(self, bottom_right):
        self.bottom_right = bottom_right

    def set_top_left_x(self, x):
        self.top_left.set_x(x)

    def get_top_left_x(self):
        return self.top_left.get_x()

    def set_top_left_y(self, y):
        self.top_left.set_y(y)

    def get_top_left_y(self):
        return self.top_left.get_y()

    def set_top_left_xy(self, x, y):
        self.top_left.set_xy(x, y)

    def get_top_left_xy(self):
        return [self.top_left.get_x(), self.top_left.get_y()]

    def set_bottom_right_x(self, x):
        self.bottom_right.set_x(x)

    def get_bottom_right_x(self):
        return self.bottom_right.get_x()

    def set_bottom_right_y(self, y):
        self.bottom_right.set_y(y)

    def get_bottom_right_y(self):
        return self.bottom_right.get_y()

    def set_bottom_right_xy(self, x, y):
        self.bottom_right.set_xy(x, y)

    def get_bottom_right_xy(self):
        return [self.bottom_right.get_x(), self.bottom_right.get_y()]

    def get_bottom_left(self):
        return MyPoint(self.top_left.get_x(), self.bottom_right.get_y())

    def get_top_right(self):
        return MyPoint(self.bottom_right.get_x(), self.top_left.get_y())

    def get_diagonal(self):
        return self.top_left.distance(another=self.bottom_right)

    def get_full_point(self):
        return f"MyRectangle[topLeft={self.top_left},bottomLeft={self.get_bottom_left()},bottomRight={self.bottom_right},topRight={self.get_top_right()}]"

    def get_area(self):
        return int(self.top_left.distance(another=self.get_top_right()) * self.bottom_right.distance(another=self.get_top_right()))

    def get_perimeter(self):
        return int((self.top_left.distance(another=self.get_top_right()) + self.bottom_right.distance(another=self.get_top_right())) * 2)

    def __str__(self):
        return f"MyRectangle[topLeft={self.top_left},bottomRight={self.bottom_right}]"


if __name__ == "__main__":
    rect2 = MyRectangle(x1=0, y1=0, x2=4, y2=3)
    print(rect2.get_full_point())