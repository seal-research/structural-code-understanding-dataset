import java.util.Arrays;

class CountEven implements Runnable {
    private int[] numbers;
    private int[] result;

    public CountEven(int[] numbers, int[] result) {
        this.numbers = numbers;
        this.result = result;
    }

    @Override
    public void run() {
        int count = (int) Arrays.stream(numbers).filter(num -> num % 2 == 0).count();
        result[0] = count;
        System.out.println("Count of even numbers: " + count);
    }
}

class CountOdd implements Runnable {
    private int[] numbers;
    private int[] result;

    public CountOdd(int[] numbers, int[] result) {
        this.numbers = numbers;
        this.result = result;
    }

    @Override
    public void run() {
        int count = (int) Arrays.stream(numbers).filter(num -> num % 2 != 0).count();
        result[1] = count;
        System.out.println("Count of odd numbers: " + count);
    }
}

public class ConcurrencyExample {
    public static void main(String[] args) throws InterruptedException {
        int[] numbers = {11, 22, 33, 44, 55, 66, 77, 88, 99, 100};
        int[] result = new int[2];

        Thread evenThread = new Thread(new CountEven(numbers, result));
        Thread oddThread = new Thread(new CountOdd(numbers, result));

        evenThread.start();
        oddThread.start();

        evenThread.join();
        oddThread.join();

        System.out.println("Total even: " + result[0] + ", Total odd: " + result[1]);
    }
}