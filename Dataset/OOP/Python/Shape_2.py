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
    c1 = Circle()
    print(c1)
    c2 = Circle(1)
    print(c2)
    c3 = Circle(2, "black", True)
    print(c3)

    c1.set_color("yellow")
    c1.set_filled(False)
    c1.set_radius(3)
    print(c1)
    print("Area:", c1.get_area())
    print("Perimeter:", c1.get_perimeter())

    r1 = Rectangle()
    print(r1)
    r2 = Rectangle(1, 2)
    print(r2)
    r3 = Rectangle(3, 4, "black", True)
    print(r3)

    r1.set_color("yellow")
    r1.set_filled(False)
    r1.set_length(5)
    r1.set_width(6)
    print(r1)
    print("Area:", r1.get_area())
    print("Perimeter:", r1.get_perimeter())

    s1 = Square()
    print(s1)
    s2 = Square(1)
    print(s2)
    s3 = Square(3, "black", True)
    print(s3)

    s1.set_color("yellow")
    s1.set_filled(False)
    s1.set_length(5)
    print(s1)
    print("Area:", s1.get_area())
    print("Perimeter:", s1.get_perimeter())