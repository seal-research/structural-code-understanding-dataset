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
    circle4 = Circle(2.5)
    print(f"Area of circle4: {circle4.get_area():.2f}, Circumference of circle4: {circle4.get_circumference():.2f}")
    circle4.radius = 4.0
    print(f"Updated Area of circle4: {circle4.get_area():.2f}, Updated Circumference of circle4: {circle4.get_circumference():.2f}")