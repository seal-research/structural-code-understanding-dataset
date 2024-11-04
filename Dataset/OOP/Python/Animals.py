class Animal:
    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        return f"Animal[name={self.name}]"


class Mammal(Animal):
    def __init__(self, name=None):
        super().__init__(name)

    def __str__(self):
        return f"Mammal[{super().__str__()}]"


class Cat(Mammal):
    def __init__(self, name=None):
        super().__init__(name)

    def greets(self):
        print("Meow")

    def __str__(self):
        return f"Cat[{super().__str__()}]"


class Dog(Mammal):
    def __init__(self, name=None):
        super().__init__(name)

    def greets(self):
        print("Woof")

    def greets_another_dog(self, another):
        print("Woooof")

    def __str__(self):
        return f"Dog[{super().__str__()}]"


if __name__ == "__main__":
    c1 = Cat("Gia Kinh")
    print(c1)
    c1.greets()
    d1 = Dog("Lan Anh")
    d2 = Dog("Noki")
    print(d1)
    print(d2)
    d1.greets()
    d1.greets_another_dog(d2)