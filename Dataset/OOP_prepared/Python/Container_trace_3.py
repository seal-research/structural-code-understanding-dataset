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
        return f"Ball[({self.x},{self.y}),speed=({self.xDelta},{self.yDelta})]"


class Container:
    def __init__(self, x1, y1, width, height):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + width - 1
        self.y2 = y1 + height - 1

    def getX1(self):
        return self.x1

    def setX1(self, x1):
        self.x1 = x1

    def getY1(self):
        return self.y1

    def setY1(self, y1):
        self.y1 = y1

    def getX2(self):
        return self.x2

    def setX2(self, x2):
        self.x2 = x2

    def getY2(self):
        return self.y2

    def setY2(self, y2):
        self.y2 = y2

    def getX(self):
        return self.x1

    def getY(self):
        return self.y1

    def getWidth(self):
        return self.x2 - self.x1 + 1

    def getHeight(self):
        return self.y2 - self.y1 + 1

    def collides(self, ball):
        if ball.getX() - ball.getRadius() <= self.x1 or ball.getX() - ball.getRadius() >= self.x2:
            ball.reflectHorizontal()
            return True
        return False

    def collidesWith(self, ball):
        if ball.getX() - ball.getRadius() <= self.x1 or ball.getX() - ball.getRadius() >= self.x2:
            ball.reflectHorizontal()
            return True
        return False

    def __str__(self):
        return f"Container[({self.x1},{self.y1}),({self.x2},{self.y2})]"


class TestContainer:
    @staticmethod
    def main():
        ball = Ball(40, 40, 5, speed=25, direction=90)
        box = Container(0, 0, 60, 60)
        for step in range(10):
            ball.move()
            box.collidesWith(ball)
            print(ball)


if __name__ == "__main__":
    TestContainer.main()