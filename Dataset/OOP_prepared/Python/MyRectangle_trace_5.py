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
        elif x1 is not None and y1 is not None and x2 is not None and y2 is not None