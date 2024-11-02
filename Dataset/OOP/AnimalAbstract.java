/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package AnimalAbstract;

import Animal.*;

/**
 *
 * @author GIA KINH
 */
abstract public class Animal {
    public abstract void greeting();
    
}

public class Dog extends Animal {

    public Dog() {
    }

    @Override
    public String toString() {
        return "Dog[" + super.toString() + ']';
    }

    @Override
    public void greeting() {
        System.out.println("Woof!");
    }

    public void greeting(Dog another) {
        System.out.println("Woooooooooof!");
    }

}

public class BigDog extends Dog {

    public BigDog() {
    }

    @Override
    public String toString() {
        return "BigDog[" + super.toString() + ']';
    }

    @Override
    public void greeting() {
        System.out.println("Woow!");
    }

    @Override
    public void greeting(Dog another) {
        System.out.println("Woooooowwwww!");
    }
}


public class Cat extends Animal {

    public Cat() {
    }

    @Override
    public String toString() {
        return "Cat[" + super.toString() + ']';
    }

    @Override
    public void greeting() {
        System.out.println("Meow!");
    }

}


/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package AnimalAbstract;

import Animal.*;

/**
 *
 * @author GIA KINH
 */
public class TestMain {

    public static void main(String[] args) {
        // Using the subclasses
        Cat cat1 = new Cat();
        cat1.greeting();
        Dog dog1 = new Dog();
        dog1.greeting();
        BigDog bigDog1 = new BigDog();
        bigDog1.greeting();

        // Using Polymorphism
        Animal animal1 = new Cat();
        animal1.greeting();
        Animal animal2 = new Dog();
        animal2.greeting();
        Animal animal3 = new BigDog();
        animal3.greeting();
        // Animal animal4 = new Animal();   // Error!!! Animal is abstract; cannot be instantiated !

        // Downcast
        Dog dog2 = (Dog)animal2;
        BigDog bigDog2 = (BigDog)animal3;
        Dog dog3 = (Dog)animal3;
        // Cat cat2 = (Cat)animal2;        // Error!!! Dog cannot be cast to Cat !

        dog2.greeting(dog3);
        dog3.greeting(dog2);
        dog2.greeting(bigDog2);
        bigDog2.greeting(dog2);
        bigDog2.greeting(bigDog1);

        bigDog1.greeting(bigDog2);
    }
}


