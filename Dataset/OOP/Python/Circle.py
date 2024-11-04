import math

class Circle:
    def __init__(self, radius=1.0):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    def get_area(self):
        return self._radius * self._radius * math.pi

    def get_circumference(self):
        return self._radius * 2 * math.pi

    def __str__(self):
        return f"Circle[radius={self._radius}]"

class TestCircle:
    @staticmethod
    def main():
        # Test Constructors and __str__()
        c1 = Circle(1.1)
        print(c1)   # __str__()
        c2 = Circle() # default constructor
        print(c2)

        # Test setter and getter
        c1.radius = 2.2
        print(c1)      # __str__()
        print(f"radius is: {c1.radius}")

        # Test get_area() and get_circumference()
        print(f"area is: {c1.get_area():.2f}")
        print(f"circumference is: {c1.get_circumference():.2f}")

if __name__ == "__main__":
    TestCircle.main()