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
public abstract class Animal {
       private String name;

    public Animal(String name) {
        this.name = name;
    }

    public Animal() {
    }
    
    
    
    public abstract void greets();
    
}

public class Dog extends Animal{

    public Dog() {
    }

    public Dog(String name) {
        super(name);
    }

    @Override
    public String toString() {
        return "Dog[" + super.toString() +']';
    } 

    @Override
    public void greets() {
        System.out.println("Woow");
    }
    
     public void greets(Dog another) {
        System.out.println("Woooooow");
    }
    
}


public class BigDog extends Dog{

    public BigDog() {
    }

    public BigDog(String name) {
        super(name);
    }

    @Override
    public String toString() {
        return "BigDog[" + super.toString() + ']';
    }
   
    @Override
    public void greets(Dog another) {
        System.out.println("Woooooow");
    }
    
    public void greets(BigDog another) {
        System.out.println("Wooooooooow");
    }
}


public class Cat extends Animal{

    public Cat(String name) {
        super(name);
    }

    public Cat() {
    }

    @Override
    public String toString() {
        return "Cat[" + super.toString() +']';
    }
    
    

    @Override
    public void greets() {
        System.out.println("Meow");
    }
    
}


public class TestMain {
    public static void main(String[] args) {
         Cat c1 = new Cat("Niko");
        c1.greets();
        Dog d1 = new Dog("Rubi");
        d1.greets();
        BigDog bD1 = new BigDog("Laiso");
        
        Animal a1 = new Cat("Niko");
        a1.greets();
        Animal a2 = new Dog("Top");
        a2.greets();
        Animal a3 = new BigDog("Ky");
        a3.greets();
        
        Dog d2 = (Dog) a2;
        BigDog bD2 = (BigDog) a3;
        Dog d3 = (Dog) a3;
        
        d2.greets(d3);
        d3.greets(d2);
        
        d2.greets(bD2);
        bD2.greets(d2);
        
        bD2.greets(bD1);
        bD1.greets(bD2);
    }
}


