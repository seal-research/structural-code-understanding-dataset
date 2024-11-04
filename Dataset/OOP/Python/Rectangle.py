class Rectangle:
    def __init__(self, length=1.0, width=1.0):
        self.length = length
        self.width = width

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width

    def get_area(self):
        return self.length * self.width

    def get_perimeter(self):
        return (self.length + self.width) * 2

    def __str__(self):
        return f"Rectangle[length={self.length}, width={self.width}]"


class TestRectangle:
    @staticmethod
    def main():
        # Test constructors and __str__()
        r1 = Rectangle(1.2, 3.4)
        print(r1)  # __str__()
        r2 = Rectangle()  # default constructor
        print(r2)

        # Test setters and getters
        r1.set_length(5.6)
        r1.set_width(7.8)
        print(r1)  # __str__()
        print(f"length is: {r1.get_length()}")
        print(f"width is: {r1.get_width()}")

        # Test get_area() and get_perimeter()
        print(f"area is: {r1.get_area():.2f}")
        print(f"perimeter is: {r1.get_perimeter():.2f}")


if __name__ == "__main__":
    TestRectangle.main()