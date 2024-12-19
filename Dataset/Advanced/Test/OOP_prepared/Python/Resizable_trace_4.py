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
    g5 = ResizableCircle(6.0)
    g5.resize(50)
    print(g5)
    print(f"New area after resizing: {g5.get_area()}")
    print(f"New perimeter after resizing: {g5.get_perimeter()}")