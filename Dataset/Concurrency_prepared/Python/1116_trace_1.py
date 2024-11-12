class ZeroEvenOdd:
  def __init__(self, n):
    self.n = n
    self.zeroSemaphore = Semaphore(1)
    self.evenSemaphore = Semaphore(0)
    self.oddSemaphore = Semaphore(0)

  # printNumber(x) outputs "x", where x is an integer.
  def zero(self, printNumber: 'Callable[[int], None]') -> None:
    for i in range(self.n):
      self.zeroSemaphore.acquire()
      printNumber(0)
      (self.oddSemaphore if i & 2 == 0 else self.evenSemaphore).release()

  def even(self, printNumber: 'Callable[[int], None]') -> None:
    for i in range(2, self.n + 1, 2):
      self.evenSemaphore.acquire()
      printNumber(i)
      self.zeroSemaphore.release()

  def odd(self, printNumber: 'Callable[[int], None]') -> None:
    for i in range(1, self.n + 1, 2):
      self.oddSemaphore.acquire()
      printNumber(i)
      self.zeroSemaphore.release()

if __name__ == "__main__":
  def printNumber(x):
    print(x, end='')

  n = 5
  zeroEvenOdd = ZeroEvenOdd(n)
  
  # Start threads for zero, even, and odd functions
  t1 = Thread(target=zeroEvenOdd.zero, args=(printNumber,))
  t2 = Thread(target=zeroEvenOdd.even, args=(printNumber,))
  t3 = Thread(target=zeroEvenOdd.odd, args=(printNumber,))
  
  t1.start() #START

  t2.start()
  t3.start()

  t1.join()
  t2.join()
  t3.join() #END


  print("\nAll threads have finished.")

