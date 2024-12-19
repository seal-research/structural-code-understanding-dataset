package Animal;

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

public class Mammal extends Animal {

    public Mammal() {
    }

    public Mammal(String name) {
        super(name);
    }

    @Override
    public String toString() {
        return "Mammal[" + super.toString() + ']';
    }
}

public class Cat extends Mammal {

    public Cat() {
    }

    public Cat(String name) {
        super(name);
    }

    public void greets() {
        System.out.println("Meow");
    }

    @Override
    public String toString() {
        return "Cat[" + super.toString() + ']';
    }
}

public class Dog extends Mammal {

    public Dog() {
    }

    public Dog(String name) {
        super(name);
    }

    public void greets() {
        System.out.println("Woof");
    }

    public void greets(Dog another) {
        System.out.println("Woooof");
    }

    @Override
    public String toString() {
        return "Dog[" + super.toString() + ']';
    }
}

public class TestMain {

    public static void main(String[] args) {
        Dog d1 = new Dog("Buddy");
        System.out.println(d1);
        d1.greets();
    }
}