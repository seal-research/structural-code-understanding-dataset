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
        for i in range(1, 4):
            print(f"Enqueueing: {i}")
            queue.enqueue(i)

    def dequeue_elements():
        print(f"Dequeued: {queue.dequeue()}")
        print(f"Dequeued: {queue.dequeue()}")
        print(f"Dequeued: {queue.dequeue()}")

    # Create threads
    t1 = Thread(target=enqueue_elements)
    t2 = Thread(target=dequeue_elements)
    t3 = Thread(target=enqueue_elements)

    t1.start() #START


    t2.start()
    t3.start()

    # Wait for all threads to finish
    t1.join()
    t2.join()
    t3.join() #END

    
    print("All threads have finished.")