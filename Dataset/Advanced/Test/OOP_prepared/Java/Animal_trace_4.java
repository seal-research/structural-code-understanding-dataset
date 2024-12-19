package Animal;

public abstract class Animal {
    private String name;

    public Animal(String name) {
        this.name = name;
    }

    public Animal() {
    }

    public abstract void greets();
}

public class Dog extends Animal {
    public Dog() {
    }

    public Dog(String name) {
        super(name);
    }

    @Override
    public String toString() {
        return "Dog[" + super.toString() + ']';
    }

    @Override
    public void greets() {
        System.out.println("Woow");
    }

    public void greets(Dog another) {
        System.out.println("Woooooow");
    }
}

public class BigDog extends Dog {
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

public class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }

    public Cat() {
    }

    @Override
    public String toString() {
        return "Cat[" + super.toString() + ']';
    }

    @Override
    public void greets() {
        System.out.println("Meow");
    }
}

public class TestMain {
    public static void main(String[] args) {
        BigDog bD1 = new BigDog("Zeus");
        Dog d1 = new Dog("Apollo");
        bD1.greets(d1);
    }
}