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
        self.radius = radius

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def __str__(self):
        return f"Circle[radius={self.radius}]"

    def get_area(self):
        return self.radius * self.radius * math.pi

    def get_perimeter(self):
        return self.radius * 2 * math.pi

class Rectangle(GeometricObject):
    def __init__(self, width=0.0, length=0.0):
        self.width = width
        self.length = length

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length

    def __str__(self):
        return f"Rectangle[width={self.width}, length={self.length}]"

    def get_area(self):
        return self.width * self.length

    def get_perimeter(self):
        return (self.width + self.length) * 2

if __name__ == "__main__":
    c = Circle(3.5)
    print("Area:", c.get_area())