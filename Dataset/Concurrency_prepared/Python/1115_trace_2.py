from threading import Semaphore
import threading

class FooBar:
  def __init__(self, n):
    self.n = n
    self.fooSemaphore = Semaphore(1)
    self.barSemaphore = Semaphore(0)

  def foo(self, printFoo: 'Callable[[], None]') -> None:
    for _ in range(self.n):
      self.fooSemaphore.acquire()
      printFoo()
      self.barSemaphore.release()

  def bar(self, printBar: 'Callable[[], None]') -> None:
    for _ in range(self.n):
      self.barSemaphore.acquire()
      printBar()
      self.fooSemaphore.release()

def printFoo():
  print("foo", end='')

def printBar():
  print("bar", end='')

if __name__ == "__main__":
  n = 3
  foobar = FooBar(n)
  thread1 = threading.Thread(target=foobar.foo, args=(printFoo,))
  thread2 = threading.Thread(target=foobar.bar, args=(printBar,))
  thread1.start()
  thread2.start()
  thread1.join()
  thread2.join()