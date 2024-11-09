import math

class Ball:
    def __init__(self, x, y, radius, xDelta=None, yDelta=None, speed=None, direction=None):
        self.x = x
        self.y = y
        self.radius = radius
        if xDelta is not None and yDelta is not None:
            self.xDelta = xDelta
            self.yDelta = yDelta
        elif speed is not None and direction is not None:
            self.xDelta = speed * math.cos(math.radians(direction))
            self.yDelta = -speed * math.sin(math.radians(direction))
        else:
            raise ValueError("Either (xDelta, yDelta) or (speed, direction) must be provided")

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def getRadius(self):
        return self.radius

    def setRadius(self, radius):
        self.radius = radius

    def getXDelta(self):
        return self.xDelta

    def setXDelta(self, xDelta):
        self.xDelta = xDelta

    def getYDelta(self):
        return self.yDelta

    def setYDelta(self, yDelta):
        self.yDelta = yDelta

    def getSpeed(self):
        return int(math.sqrt(self.xDelta * self.xDelta + self.yDelta * self.yDelta))

    def getDirection(self):
        return int(math.degrees(math.atan2(-self.yDelta, self.xDelta)))

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.xDelta
        self.y += self.yDelta

    def reflectHorizontal(self):
        self.xDelta = -self.xDelta

    def reflectVertical(self):
        self.yDelta = -self.yDelta

    def __str__(self):
        return f"Ball[({self.x},{self.y}),speed=({self.xDelta},{self.y