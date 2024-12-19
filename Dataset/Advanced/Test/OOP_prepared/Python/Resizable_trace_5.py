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

if __name__ == "__main__":
    g3 = ResizableCircle(4.0)
    print(g3)
    g3.resize(200)
    print(g3)

    g4 = Circle(10.0)
    g4.radius = 15.0
    print(f"Updated area: {g4.get_area()}")
    print(f"Updated perimeter: {g4.get_perimeter()}")