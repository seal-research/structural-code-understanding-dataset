/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Animal;

/**
 *
 * @author GIA KINH
 */
public class Animal {
    private String name;

    public Animal() {
    }


    public Animal(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Animal[" + "name=" + name + ']';
    }
    
    
}

public class Mammal extends Animal{

    public Mammal() {
    }

    public Mammal(String name) {
        super(name);
    }

    
    @Override
    public String toString() {
        return "Mammal["+super.toString() + ']';
    }  
}


public class Cat extends Mammal{

    public Cat() {
    }

    public Cat(String name) {
        super(name);
    }
    
    public void greets(){
        System.out.println("Meow");
    }
    
    @Override
    public String toString() {
        return "Cat[" + super.toString() + ']';
    }
}


public class Dog extends Mammal{

    public Dog() {
    }

    public Dog(String name) {
        super(name);
    }
    
    public void greets(){
        System.out.println("Woof");
    }
    
    public void greets(Dog another){
        System.out.println("Woooof");
    }

    @Override
    public String toString() {
        return "Dog[" + super.toString() + ']';
    }
}


public class TestMain {

    public static void main(String[] args) {
        Cat c1 = new Cat("Gia Kinh");
        System.out.println(c1);
        c1.greets();
        Dog d1 = new Dog("Lan Anh");
        Dog d2 = new Dog("Noki");
        System.out.println(d1);
        System.out.println(d2);
        d1.greets();
        d1.greets(d2);
    }
}


