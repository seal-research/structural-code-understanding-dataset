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
    circle3 = Circle()
    print(f"Default Area of circle3: {circle3.get_area():.2f}, Default Circumference of circle3: {circle3.get_circumference():.2f}")
    circle3.radius = 7.5
    print(f"Updated Area of circle3: {circle3.get_area():.2f}, Updated Circumference of circle3: {circle3.get_circumference():.2f}")