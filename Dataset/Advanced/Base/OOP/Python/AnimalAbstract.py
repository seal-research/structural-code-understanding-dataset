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
    # Using the subclasses
    cat1 = Cat()
    cat1.greeting()
    dog1 = Dog()
    dog1.greeting()
    bigDog1 = BigDog()
    bigDog1.greeting()

    # Using Polymorphism
    animal1 = Cat()
    animal1.greeting()
    animal2 = Dog()
    animal2.greeting()
    animal3 = BigDog()
    animal3.greeting()
    # animal4 = Animal()   # Error!!! Animal is abstract; cannot be instantiated !

    # Downcast
    dog2 = animal2
    bigDog2 = animal3
    dog3 = animal3
    # cat2 = animal2        # Error!!! Dog cannot be cast to Cat !

    dog2.greeting_dog(dog3)
    dog3.greeting_dog(dog2)
    dog2.greeting_dog(bigDog2)
    bigDog2.greeting_dog(dog2)
    bigDog2.greeting_dog(bigDog1)

    bigDog1.greeting_dog(bigDog2)

if __name__ == "__main__":
    main()