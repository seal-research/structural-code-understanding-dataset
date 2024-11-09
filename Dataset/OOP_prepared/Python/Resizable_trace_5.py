import math
from abc import ABC, abstractmethod

class GeometricObject(ABC):
    @abstractmethod
    def get_area(self):
        pass

    @abstractmethod
    def get_perimeter(self):
        pass

class Circle(GeometricObject):
    def __init__(self, radius=0.0):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    def __str__(self):
        return f"Circle[radius={self._radius}]"

    def get_area(self):
        return self._radius * self._radius * math.pi

    def get_perimeter(self):
        return self._radius * 2 * math.pi

class Resizable(ABC):
    @abstractmethod
    def resize(self, percent):
        pass

class ResizableCircle(Circle, Resizable):
    def __init__(self, radius=0.0):
        super().__init__(radius)

    def __str__(self):
        return f"ResizableCircle[{super().__str__()}]"

    def resize(self, percent):
        self._radius *= percent / 100

class TestMain:
    @staticmethod
    def main():
        g1 = Circle(1.2)
        print(g1)
        print(f"Perimeter = {g1.get_perimeter()}")
        print(f"Area = {g1.get_area()}")

        g2 = ResizableCircle(3.4)
        print(g2)
        g2.resize(56)
        print(g2)

        g3 = g2  # In Python, no need to cast explicitly
        print(g3)
        print(f"Perimeter = {g3.get_perimeter()}")
        print(f"Area = {g3.get_area()}")

if __name__ == "__main__":
    g1 = Circle(8.1)
    print(g1)
    print(f"Perimeter = {g1.get_perimeter()}")
    print(f"Area = {g1.get_area()}")