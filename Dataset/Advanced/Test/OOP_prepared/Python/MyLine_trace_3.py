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
        return f"({self.x}, {self.y})"


class MyLine:
    def __init__(self, x1=None, y1=None, x2=None, y2=None, begin=None, end=None):
        if begin is not None and end is not None:
            self.begin = begin
            self.end = end
        else:
            self.begin = MyPoint(x1, y1)
            self.end = MyPoint(x2, y2)

    def get_begin(self):
        return self.begin

    def set_begin(self, begin):
        self.begin = begin

    def get_end(self):
        return self.end

    def set_end(self, end):
        self.end = end

    def set_begin_x(self, x):
        self.begin.set_x(x)

    def get_begin_x(self):
        return self.begin.get_x()

    def set_begin_y(self, y):
        self.begin.set_y(y)

    def get_begin_y(self):
        return self.begin.get_y()

    def set_end_x(self, x):
        self.end.set_x(x)

    def get_end_x(self):
        return self.end.get_x()

    def set_end_y(self, y):
        self.end.set_y(y)

    def get_end_y(self):
        return self.end.get_y()

    def set_begin_xy(self, x, y):
        self.begin.set_xy(x, y)

    def get_begin_xy(self):
        return self.begin.get_xy()

    def set_end_xy(self, x, y):
        self.end.set_xy(x, y)

    def get_end_xy(self):
        return self.end.get_xy()

    def get_length(self):
        return self.begin.distance(another=self.end)

    def get_gradient(self):
        return math.atan2(self.end.get_y() - self.begin.get_y(), self.end.get_x() - self.begin.get_x())

    def __str__(self):
        return f"MyLine[begin={self.begin}, end={self.end}]"


class TestMyLine:
    @staticmethod
    def main():
        my_line = MyLine(begin=MyPoint(3, 4), end=MyPoint(6, 8))
        print(my_line.get_length())


if __name__ == "__main__":
    line1 = MyLine(1, 2, 3, 4)
    print(line1.get_length())