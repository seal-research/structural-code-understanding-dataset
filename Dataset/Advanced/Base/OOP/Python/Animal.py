class Animal:
    def __init__(self, name=None):
        self.name = name

    def greets(self):
        raise NotImplementedError("Subclasses should implement this!")


class Dog(Animal):
    def __init__(self, name=None):
        super().__init__(name)

    def __str__(self):
        return f"Dog[{super().__str__()}]"

    def greets(self):
        print("Woow")

    def greets_dog(self, another):
        print("Woooooow")


class BigDog(Dog):
    def __init__(self, name=None):
        super().__init__(name)

    def __str__(self):
        return f"BigDog[{super().__str__()}]"

    def greets_dog(self, another):
        print("Woooooow")

    def greets_bigdog(self, another):
        print("Wooooooooow")


class Cat(Animal):
    def __init__(self, name=None):
        super().__init__(name)

    def __str__(self):
        return f"Cat[{super().__str__()}]"

    def greets(self):
        print("Meow")


if __name__ == "__main__":
    c1 = Cat("Niko")
    c1.greets()
    d1 = Dog("Rubi")
    d1.greets()
    bD1 = BigDog("Laiso")

    a1 = Cat("Niko")
    a1.greets()
    a2 = Dog("Top")
    a2.greets()
    a3 = BigDog("Ky")
    a3.greets()

    d2 = a2
    bD2 = a3
    d3 = a3

    d2.greets_dog(d3)
    d3.greets_dog(d2)

    d2.greets_dog(bD2)
    bD2.greets_dog(d2)

    bD2.greets_bigdog(bD1)
    bD1.greets_bigdog(bD2)