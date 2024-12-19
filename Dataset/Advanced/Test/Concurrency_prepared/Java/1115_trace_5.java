class FooBar {
  public FooBar(int n) {
    this.n = n;
  }

  public void foo(Runnable printFoo) throws InterruptedException {
    for (int i = 0; i < n; ++i) {
      fooSemaphore.acquire();
      printFoo.run();
      barSemaphore.release();
    }
  }

  public void bar(Runnable printBar) throws InterruptedException {
    for (int i = 0; i < n; ++i) {
      barSemaphore.acquire();
      printBar.run();
      fooSemaphore.release();
    }
  }

  private int n;
  private Semaphore fooSemaphore = new Semaphore(1);
  private Semaphore barSemaphore = new Semaphore(0);

  public static void main(String[] args) throws InterruptedException {
    FooBar fooBar = new FooBar(6);
    Runnable printFoo = () -> System.out.print("foo");
    Runnable printBar = () -> System.out.print("bar");

    Thread threadFoo = new Thread(() -> {
      try {
        fooBar.foo(printFoo);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    });

    Thread threadBar = new Thread(() -> {
      try {
        fooBar.bar(printBar);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    });

    threadFoo.start();
    threadBar.start();

    threadFoo.join();
    threadBar.join();
  }
}