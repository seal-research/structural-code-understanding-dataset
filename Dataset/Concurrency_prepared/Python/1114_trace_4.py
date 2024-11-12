from threading import Lock

class Foo:
  def __init__(self):
    self.firstDone = Lock()
    self.secondDone = Lock()
    self.firstDone.acquire()
    self.secondDone.acquire()

  def first(self, printFirst: 'Callable[[], None]') -> None:
    printFirst()
    self.firstDone.release()

  def second(self, printSecond: 'Callable[[], None]') -> None:
    self.firstDone.acquire()
    printSecond()
    self.secondDone.release()

  def third(self, printThird: 'Callable[[], None]') -> None:
    self.secondDone.acquire()
    printThird()

if __name__ == "__main__":
  foo = Foo()
    
  def run_first():
      foo.first(lambda: print("First"))
  
  def run_second():
      foo.second(lambda: print("Second"))
  
  def run_third():
      foo.third(lambda: print("Third"))

  t1 = Thread(target=run_first)
  t2 = Thread(target=run_second)
  t3 = Thread(target=run_third)

  t1.start()
  #START
  t3.start()
  t2.start()

  t1.join()
  t2.join()
  t3.join()