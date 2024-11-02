class FactorialCalculator {
    public static int factorial(int n) {
        if (n == 0 || n == 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
}

class EvenFactorial implements Runnable {
    private int[] numbers;
    private int[] result;

    public EvenFactorial(int[] numbers, int[] result) {
        this.numbers = numbers;
        this.result = result;
    }

    @Override
    public void run() {
        int count = 0;
        for (int num : numbers) {
            if (num % 2 == 0) {
                count += FactorialCalculator.factorial(num);
            }
        }
        result[0] = count;
        System.out.println("Sum of factorials of even numbers: " + count);
    }
}

class OddFactorial implements Runnable {
    private int[] numbers;
    private int[] result;

    public OddFactorial(int[] numbers, int[] result) {
        this.numbers = numbers;
        this.result = result;
    }

    @Override
    public void run() {
        int count = 0;
        for (int num : numbers) {
            if (num % 2 != 0) {
                count += FactorialCalculator.factorial(num);
            }
        }
        result[1] = count;
        System.out.println("Sum of factorials of odd numbers: " + count);
    }
}

public class ConcurrencyFactorialExample {
    public static void main(String[] args) throws InterruptedException {
        int[] numbers = {1, 2, 3, 4, 5, 6};
        int[] result = new int[2];

        Thread evenThread = new Thread(new EvenFactorial(numbers, result));
        Thread oddThread = new Thread(new OddFactorial(numbers, result));

        evenThread.start();
        oddThread.start();

        evenThread.join();
        oddThread.join();

        System.out.println("Total sum of even factorials: " + result[0] + ", Total sum of odd factorials: " + result[1]);
    }
}
