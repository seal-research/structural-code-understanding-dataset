import math

class MyComplex:
    def __init__(self, real=0.0, imag=0.0):
        self.real = real
        self.imag = imag

    def get_real(self):
        return self.real

    def set_real(self, real):
        self.real = real

    def get_imag(self):
        return self.imag

    def set_imag(self, imag):
        self.imag = imag

    def __str__(self):
        return f"({self.real}+{self.imag}i)"

    def is_real(self):
        return self.real == 0

    def is_imaginary(self):
        return self.imag == 0

    def equals(self, real, imag):
        return self.real == real and self.imag == imag

    def equals_complex(self, another):
        return self.real == another.real and self.imag == another.imag

    def magnitude(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def argument(self):
        return math.atan2(self.imag, self.real)

    def add_into(self, right):
        self.real += right.real
        self.imag += right.imag
        return self

    def add(self, right):
        self.real += right.real
        self.imag += right.imag
        return self

    def add_new(self, right):
        return MyComplex(self.real + right.real, self.imag + right.imag)

    def subtract(self, right):
        self.real -= right.real
        self.imag -= right.imag
        return self

    def subtract_new(self, right):
        return MyComplex(self.real - right.real, self.imag - right.imag)

    def multiply(self, right):
        real = self.real * right.real - self.imag * right.imag
        imag = self.real * right.imag + self.imag * right.real
        self.real = real
        self.imag = imag
        return self

    def divide(self, right):
        denominator = right.real**2 + right.imag**2
        real = (self.real * right.real + self.imag * right.imag) / denominator
        imag = (self.imag * right.real - self.real * right.imag) / denominator
        self.real = real
        self.imag = imag
        return self

    def conjugate(self):
        self.imag *= -1
        return self

if __name__ == "__main__":
    c7 = MyComplex(3, 4)
    c8 = MyComplex(1, 2)
    result = c7.subtract_new(c8)