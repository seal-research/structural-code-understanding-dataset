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


if __name__ == "__main__":
    r5 = Rectangle(6.0, 3.0)
    print(r5.get_perimeter())