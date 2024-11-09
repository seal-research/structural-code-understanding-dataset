from math import pi

class Shape:
    def __init__(self, color="red", filled=True):
        self.color = color
        self.filled = filled

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def is_filled(self):
        return self.filled

    def set_filled(self, filled):
        self.filled = filled

    def get_area(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_perimeter(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def __str__(self):
        return f"Shape[color={self.color}, filled={self.filled}]"


class Circle(Shape):
    def __init__(self, radius=1.0, color="red", filled=True):
        super().__init__(color, filled)
        self.radius = radius

    def get_area(self):
        return self.radius * self.radius * pi

    def get_perimeter(self):
        return 2 * self.radius * pi

    def __str__(self):
        return f"Circle[{super().__str__()}, radius={self.radius}]"

    def set_radius(self, radius):
        self.radius = radius


class Rectangle(Shape):
    def __init__(self, width=1.0, length=1.0, color="red", filled=True):
        super().__init__(color, filled)
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

    def get_area(self):
        return self.width * self.length

    def get_perimeter(self):
        return 2 * (self.width + self.length)

    def __str__(self):
        return f"Rectangle[{super().__str__()}, width={self.width}, length={self.length}]"


class Square(Rectangle):
    def __init__(self, side=1.0, color="red", filled=True):
        super().__init__(side, side, color, filled)

    def get_side(self):
        return self.get_length()

    def set_width(self, side):
        super().set_width(side)
        super().set_length(side)

    def set_length(self, side):
        super().set_width(side)
        super().set_length(side)

    def __str__(self):
        return f"Square[{super().__str__()}]"


if __name__ == "__main__":
    c2 = Circle(10)
    print(c2.get_area())