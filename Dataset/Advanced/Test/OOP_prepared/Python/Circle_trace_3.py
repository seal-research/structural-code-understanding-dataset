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


if __name__ == "__main__":
    circle2 = Circle(10.0)
    circle2.radius = 12.0
    print(f"Updated Area of circle2: {circle2.get_area():.2f}, Updated Circumference of circle2: {circle2.get_circumference():.2f}")