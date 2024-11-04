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

# Test program to test all constructors and public methods
if __name__ == "__main__":
    p1 = MyPoint()  # Test constructor
    print(p1)       # Test __str__()
    p1.set_x(8)     # Test setters
    p1.set_y(6)
    print("x is:", p1.get_x())  # Test getters
    print("y is:", p1.get_y())
    p1.set_xy(3, 0)  # Test set_xy()
    print(p1.get_xy()[0])  # Test get_xy()
    print(p1.get_xy()[1])
    print(p1)

    p2 = MyPoint(0, 4)  # Test another constructor
    print(p2)
    # Testing the overloaded methods distance()
    print(p1.distance(another=p2))  # which version?
    print(p2.distance(another=p1))  # which version?
    print(p1.distance(5, 6))  # which version?
    print(p1.distance())      # which version?