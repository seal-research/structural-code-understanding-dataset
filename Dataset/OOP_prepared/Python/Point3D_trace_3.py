class Point2D:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    def set_xy(self, x, y):
        self._x = x
        self._y = y

    def get_xy(self):
        return [self._x, self._y]

    def __str__(self):
        return f"({self._x}, {self._y})"


class Point3D(Point2D):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y)
        self._z = z

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z

    def set_xyz(self, x, y, z):
        self.set_xy(x, y)
        self._z = z

    def get_xyz(self):
        return [self.x, self.y, self._z]

    def __str__(self):
        return f"({self.x}, {self.y}, {self._z})"


if __name__ == "__main__":
    p3 = Point3D(1, 2, 3)
    print(p3.get_xyz())