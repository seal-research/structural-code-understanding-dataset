class Ball:
    def __init__(self, x, y, radius, xDelta, yDelta):
        self.x = x
        self.y = y
        self.radius = radius
        self.xDelta = xDelta
        self.yDelta = yDelta

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

    def move(self):
        self.x += self.xDelta
        self.y += self.yDelta

    def reflectHorizontal(self):
        self.xDelta = -self.xDelta

    def reflectVertical(self):
        self.yDelta = -self.yDelta

    def __str__(self):
        return f"Ball[({self.x},{self.y}),speed=({self.xDelta},{self.yDelta})]"


def main():
    # Test constructor and __str__()
    ball = Ball(1.1, 2.2, 10, 3.3, 4.4)
    print(ball)  # __str__()

    # Test Setters and Getters
    ball.setX(80.0)
    ball.setY(35.0)
    ball.setRadius(5)
    ball.setXDelta(4.0)
    ball.setYDelta(6.0)
    print(ball)  # __str__()
    print("x is:", ball.getX())
    print("y is:", ball.getY())
    print("radius is:", ball.getRadius())
    print("xDelta is:", ball.getXDelta())
    print("yDelta is:", ball.getYDelta())

    # Bounce the ball within the boundary
    xMin = 0.0
    xMax = 100.0
    yMin = 0.0
    yMax = 50.0
    for _ in range(15):
        ball.move()
        print(ball)
        xNew = ball.getX()
        yNew = ball.getY()
        radius = ball.getRadius()
        # Check boundary value to bounce back
        if (xNew + radius) > xMax or (xNew - radius) < xMin:
            ball.reflectHorizontal()
        if (yNew + radius) > yMax or (yNew - radius) < yMin:
            ball.reflectVertical()


if __name__ == "__main__":
    main()