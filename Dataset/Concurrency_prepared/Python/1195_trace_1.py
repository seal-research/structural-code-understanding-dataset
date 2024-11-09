from threading import Semaphore


class FizzBuzz:
  def __init__(self, n: int):
    self.n = n
    self.fizzSemaphore = Semaphore(0)
    self.buzzSemaphore = Semaphore(0)
    self.fizzbuzzSemaphore = Semaphore(0)
    self.numberSemaphore = Semaphore(1)

  # printFizz() outputs "fizz"
  def fizz(self, printFizz: 'Callable[[], None]') -> None:
    for i in range(1, self.n + 1):
      if i % 3 == 0 and i % 15 != 0:
        self.fizzSemaphore.acquire()
        printFizz()
        self.numberSemaphore.release()

  # printBuzz() outputs "buzz"
  def buzz(self, printBuzz: 'Callable[[], None]') -> None:
    for i in range(1, self.n + 1):
      if i % 5 == 0 and i % 15 != 0:
        self.buzzSemaphore.acquire()
        printBuzz()
        self.numberSemaphore.release()

  # printFizzBuzz() outputs "fizzbuzz"
  def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
    for i in range(1, self.n + 1):
      if i % 15 == 0:
        self.fizzbuzzSemaphore.acquire()
        printFizzBuzz()
        self.numberSemaphore.release()

  # printNumber(x) outputs "x", where x is an integer.
  def number(self, printNumber: 'Callable[[int], None]') -> None:
    for i in range(1, self.n + 1):
      self.numberSemaphore.acquire()
      if i % 15 == 0:
        self.fizzbuzzSemaphore.release()
      elif i % 3 == 0:
        self.fizzSemaphore.release()
      elif i % 5 == 0:
        self.buzzSemaphore.release()
      else:
        printNumber(i)
        self.numberSemaphore.release()


if __name__ == "__main__":
  import threading

  def printFizz():
    print("fizz", end=' ')

  def printBuzz():
    print("buzz", end=' ')

  def printFizzBuzz():
    print("fizzbuzz", end=' ')

  def printNumber(x):
    print(x, end=' ')

  n = 15
  fizzbuzz = FizzBuzz(n)

  threads = [
    threading.Thread(target=fizzbuzz.fizz, args=(printFizz,)),
    threading.Thread(target=fizzbuzz.buzz, args=(printBuzz,)),
    threading.Thread(target=fizzbuzz.fizzbuzz, args=(printFizzBuzz,)),
    threading.Thread(target=fizzbuzz.number, args=(printNumber,))
  ]

  for t in threads:
    t.start()
  for t in threads:
    t.join()