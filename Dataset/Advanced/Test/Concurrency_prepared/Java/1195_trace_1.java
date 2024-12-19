class FizzBuzz {
  public FizzBuzz(int n) {
    this.n = n;
  }

  // printFizz.run() outputs "fizz".
  public void fizz(Runnable printFizz) throws InterruptedException {
    for (int i = 1; i <= n; ++i)
      if (i % 3 == 0 && i % 15 != 0) {
        fizzSemaphore.acquire();
        printFizz.run();
        numberSemaphore.release();
      }
  }

  // printBuzz.run() outputs "buzz".
  public void buzz(Runnable printBuzz) throws InterruptedException {
    for (int i = 1; i <= n; ++i)
      if (i % 5 == 0 && i % 15 != 0) {
        buzzSemaphore.acquire();
        printBuzz.run();
        numberSemaphore.release();
      }
  }

  // printFizzBuzz.run() outputs "fizzbuzz".
  public void fizzbuzz(Runnable printFizzBuzz) throws InterruptedException {
    for (int i = 1; i <= n; ++i)
      if (i % 15 == 0) {
        fizzbuzzSemaphore.acquire();
        printFizzBuzz.run();
        numberSemaphore.release();
      }
  }

  // printNumber.accept(x) outputs "x", where x is an integer.
  public void number(IntConsumer printNumber) throws InterruptedException {
    for (int i = 1; i <= n; ++i) {
      numberSemaphore.acquire();
      if (i % 15 == 0)
        fizzbuzzSemaphore.release();
      else if (i % 3 == 0)
        fizzSemaphore.release();
      else if (i % 5 == 0)
        buzzSemaphore.release();
      else {
        printNumber.accept(i);
        numberSemaphore.release();
      }
    }
  }

  private int n;
  private Semaphore fizzSemaphore = new Semaphore(0);
  private Semaphore buzzSemaphore = new Semaphore(0);
  private Semaphore fizzbuzzSemaphore = new Semaphore(0);
  private Semaphore numberSemaphore = new Semaphore(1);

  public static void main(String[] args) throws InterruptedException {
    FizzBuzz fb = new FizzBuzz(15);
    Thread t1 = new Thread(() -> {
      try {
        fb.fizz(() -> System.out.print("fizz "));
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    });
    Thread t2 = new Thread(() -> {
      try {
        fb.buzz(() -> System.out.print("buzz "));
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    });
    Thread t3 = new Thread(() -> {
      try {
        fb.fizzbuzz(() -> System.out.print("fizzbuzz "));
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    });
    Thread t4 = new Thread(() -> {
      try {
        fb.number(System.out::print);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    });

    t1.start();
    t2.start();
    t3.start();
    t4.start();

    t1.join();
    t2.join();
    t3.join();
    t4.join();
  }
}