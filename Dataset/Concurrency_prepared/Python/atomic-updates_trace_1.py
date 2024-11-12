terminate = threading.Event()

class Buckets:
    def __init__(self, nbuckets):
        self.nbuckets = nbuckets
        self.values = [random.randrange(10) for i in range(nbuckets)]
        self.lock = threading.Lock()

    def __getitem__(self, i):
        return self.values[i]

    def transfer(self, src, dst, amount):
        with self.lock:
            amount = min(amount, self.values[src])
            self.values[src] -= amount
            self.values[dst] += amount

    def snapshot(self):
        # copy of the current state (synchronized)
        with self.lock:
            return self.values[:]

def randomize(buckets):
    nbuckets = buckets.nbuckets
    while not terminate.isSet():
        src = random.randrange(nbuckets)
        dst = random.randrange(nbuckets)
        if dst!=src:
            amount = random.randrange(20)
            buckets.transfer(src, dst, amount)

def equalize(buckets):
    nbuckets = buckets.nbuckets
    while not terminate.isSet():
        src = random.randrange(nbuckets)
        dst = random.randrange(nbuckets)
        if dst!=src:
            amount = (buckets[src] - buckets[dst]) // 2
            if amount>=0: buckets.transfer(src, dst, amount)
            else: buckets.transfer(dst, src, -amount)

def print_state(buckets):
    snapshot = buckets.snapshot()
    for value in snapshot:
        print(f'{value:2d}', end=' ')  # Using f-string for formatting
    print('=', sum(snapshot))

if __name__ == "__main__":
    # create 5 buckets
    buckets = Buckets(5)

    # Create a threading event for termination signal
    terminate = threading.Event()

    t1 = threading.Thread(target=randomize, args=[buckets])
    t1.start()
    # START

    # the equalize thread
    t2 = threading.Thread(target=equalize, args=[buckets])
    t2.start()

    # main thread, display
    max_steps = 10  # Define the number of steps (iterations)
    current_step = 0

    try:
        while current_step < max_steps:
            print_state(buckets)
            time.sleep(1)
            current_step += 1
    except KeyboardInterrupt:  # ^C to finish
        terminate.set()

    # Wait until all worker threads finish
    t1.join()
    t2.join()