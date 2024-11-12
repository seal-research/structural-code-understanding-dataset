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
  def run_foo_instance(foo_instance):
        foo_instance.first(lambda: print("First"))
        foo_instance.second(lambda: print("Second"))
        foo_instance.third(lambda: print("Third"))
    
  foo1 = Foo()
  foo2 = Foo()

  t1 = Thread(target=run_foo_instance, args=(foo1,))
  t2 = Thread(target=run_foo_instance, args=(foo2,))

  t1.start()
  #START
  t2.start()

  t1.join()
  t2.join()