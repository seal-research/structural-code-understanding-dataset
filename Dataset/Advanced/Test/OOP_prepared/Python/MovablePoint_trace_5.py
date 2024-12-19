class Point:
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

    def setXY(self, x, y):
        self._x = x
        self._y = y

    def getXY(self):
        return [self._x, self._y]

    def __str__(self):
        return f"({self._x},{self._y})"


class MovablePoint(Point):
    def __init__(self, x=0.0, y=0.0, xSpeed=0.0, ySpeed=0.0):
        super().__init__(x, y)
        self._xSpeed = xSpeed
        self._ySpeed = ySpeed

    @property
    def xSpeed(self):
        return self._xSpeed

    @xSpeed.setter
    def xSpeed(self, xSpeed):
        self._xSpeed = xSpeed

    @property
    def ySpeed(self):
        return self._ySpeed

    @ySpeed.setter
    def ySpeed(self, ySpeed):
        self._ySpeed = ySpeed

    def setSpeed(self, xSpeed, ySpeed):
        self._xSpeed = xSpeed
        self._ySpeed = ySpeed

    def getSpeed(self):
        return [self._xSpeed, self._ySpeed]

    def __str__(self):
        return super().__str__() + f",speed=({self._xSpeed},{self._ySpeed})"

    def move(self):
        self.x += self._xSpeed
        self.y += self._ySpeed
        return self


if __name__ == "__main__":
    m3 = MovablePoint(5.0, 5.0, 1.0, 1.0)
    m3.setSpeed(2.0, 3.0)
    m3.move()
    print(m3)