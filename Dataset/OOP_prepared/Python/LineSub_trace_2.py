import math

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return f"Point:({self._x},{self._y})"

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_xy(self, x, y):
        self._x = x
        self._y = y


class LineSub(Point):
    def __init__(self, begin, end=None, end_x=None, end_y=None):
        if isinstance(begin, Point) and isinstance(end, Point):
            super().__init__(begin.get_x(), begin.get_y())
            self._end = end
        elif isinstance(begin, int) and isinstance(end, int) and isinstance(end_x, int) and isinstance(end_y, int):
            super().__init__(begin, end)
            self._end = Point(end_x, end_y)
        else:
            raise ValueError("Invalid arguments")

    def __str__(self):
        return f"LineSub[begin={super().__str__()},end={self._end}]"

    def get_begin(self):
        return Point(self.get_x(), self.get_y())

    def get_end(self):
        return self._end

    def set_begin(self, begin_x, begin_y):
        self.set_xy(begin_x, begin_y)

    def set_end(self, end_x, end_y):
        self._end.set_xy(end_x, end_y)

    def get_begin_x(self):
        return self.get_x()

    def get_begin_y(self):
        return self.get_y()

    def get_end_x(self):
        return self._end.get_x()

    def get_end_y(self):
        return self._end.get_y()

    def set_begin_x(self, begin_x):
        self.set_x(begin_x)

    def set_begin_y(self, begin_y):
        self.set_y(begin_y)

    def set_begin_xy(self, begin_x, begin_y):
        self.set_xy(begin_x, begin_y)

    def set_end_x(self, end_x):
        self._end.set_x(end_x)

    def set_end_y(self, end_y):
        self._end.set_y(end_y)

    def set_end_xy(self, end_x, end_y):
        self._end.set_xy(end_x, end_y)

    def get_length(self):
        return int(math.sqrt((self._end.get_x() - self.get_x()) ** 2 + (self._end.get_y() - self.get_y()) ** 2))

    def get_gradient(self):
        return math.atan2(self._end.get_y() - self.get_y(), self._end.get_x() - self.get_x())


if __name__ == "__main__":
    begin = Point(3, 4)
    end = Point(6, 8)
    line1 = LineSub(begin, end)
    print(line1.get_begin())
    print(line1.get_end())
    print(line1.get_length())
    print(line1.get_gradient())