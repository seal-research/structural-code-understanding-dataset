from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def greeting(self):
        pass

class Dog(Animal):
    def __init__(self):
        pass

    def __str__(self):
        return f"Dog[{super().__str__()}]"

    def greeting(self):
        print("Woof!")

    def greeting_dog(self, another):
        print("Woooooooooof!")

class BigDog(Dog):
    def __init__(self):
        pass

    def __str__(self):
        return f"BigDog[{super().__str__()}]"

    def greeting(self):
        print("Woow!")

    def greeting_dog(self, another):
        print("Woooooowwwww!")

class Cat(Animal):
    def __init__(self):
        pass

    def __str__(self):
        return f"Cat[{super().__str__()}]"

    def greeting(self):
        print("Meow!")

def main():
    dog1 = Dog()
    bigDog1 = BigDog()
    dog1.greeting_dog(bigDog1)

if __name__ == "__main__":
    main()