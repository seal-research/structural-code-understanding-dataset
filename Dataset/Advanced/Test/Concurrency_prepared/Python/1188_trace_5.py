class BoundedBlockingQueue:
  def __init__(self, capacity: int):
    self.q = collections.deque()
    self.enqueueSemaphore = Semaphore(capacity)
    self.dequeueSemaphore = Semaphore(0)

  def enqueue(self, element: int) -> None:
    self.enqueueSemaphore.acquire()
    self.q.append(element)
    self.dequeueSemaphore.release()

  def dequeue(self) -> int:
    self.dequeueSemaphore.acquire()
    element = self.q.popleft()
    self.enqueueSemaphore.release()
    return element

  def size(self) -> int:
    return len(self.q)

if __name__ == "__main__":
    queue = BoundedBlockingQueue(5)

    def enqueue_elements():
        for i in range(10):
            queue.enqueue(i)

    def dequeue_elements():
        for i in range(10):
            print(queue.dequeue())

    t1 = Thread(target=enqueue_elements)
    t2 = Thread(target=dequeue_elements)
    t1.start() #START

    t2.start()
    t1.join()
    t2.join()