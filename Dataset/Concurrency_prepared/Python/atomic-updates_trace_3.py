import threading
import random
import time

class Buckets:
    def __init__(self, nbuckets):
        self.nbuckets = nbuckets
        self.values = [random.randrange(10) for _ in range(nbuckets)]
        # Use a list of locks, one for each bucket to avoid deadlock
        self.locks = [threading.Lock() for _ in range(nbuckets)]

    def __getitem__(self, i):
        return self.values[i]

    def transfer(self, src, dst, amount):
        # Lock both buckets to transfer values
        with self.locks[src], self.locks[dst]:
            amount = min(amount, self.values[src])
            self.values[src] -= amount
            self.values[dst] += amount

    def snapshot(self):
        # Copy of the current state (synchronized)
        snapshot = []
        for i in range(self.nbuckets):
            with self.locks[i]:
                snapshot.append(self.values[i])
        return snapshot

def randomize(buckets, terminate):
    nbuckets = buckets.nbuckets
    while not terminate.is_set():
        src = random.randrange(nbuckets)
        dst = random.randrange(nbuckets)
        if dst != src:
            amount = random.randrange(20)
            buckets.transfer(src, dst, amount)
        time.sleep(0.01)  # Add a small delay to allow checking terminate flag

def equalize(buckets, terminate):
    nbuckets = buckets.nbuckets
    while not terminate.is_set():
        src = random.randrange(nbuckets)
        dst = random.randrange(nbuckets)
        if dst != src:
            amount = (buckets[src] - buckets[dst]) // 2
            if amount >= 0:
                buckets.transfer(src, dst, amount)
            else:
                buckets.transfer(dst, src, -amount)
        time.sleep(0.01)  # Add a small delay to allow checking terminate flag

def print_state(buckets):
    snapshot = buckets.snapshot()
    for value in snapshot:
        print(f'{value:2d}', end=' ')  # Using f-string for formatting
    print('=', sum(snapshot))

if __name__ == "__main__":
    # Create 5 buckets
    buckets = Buckets(12)

    # Create a threading event for termination signal
    terminate = threading.Event()

    # Create and start the randomize thread
    t1 = threading.Thread(target=randomize, args=(buckets, terminate))
    t1.start()#START

    # Create and start the equalize thread
    t2 = threading.Thread(target=equalize, args=(buckets, terminate))
    t2.start()

    # Main thread, display state
    max_steps = 8  # Define the number of steps (iterations)
    current_step = 0

    try:
        while current_step < max_steps:
            print_state(buckets)
            time.sleep(1)
            current_step += 1
        terminate.set()
    except KeyboardInterrupt:  # ^C to finish
        terminate.set()

    # Wait until all worker threads finish
    t1.join()
    t2.join()