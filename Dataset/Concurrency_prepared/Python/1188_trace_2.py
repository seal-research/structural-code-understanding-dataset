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
    queue = BoundedBlockingQueue(3)

    def enqueue_elements():
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)

    def dequeue_elements():
        print(queue.dequeue())  # Expected output: 1, then 2, then 3

    t1 = Thread(target=enqueue_elements)
    t2 = Thread(target=dequeue_elements)
    t1.start()
    #START
    t2.start()
    t1.join()
    t2.join()
    #END