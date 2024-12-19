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
    a = Animal("Generic Animal")
    try:
        a.greets()
    except NotImplementedError as e:
        print(e)  