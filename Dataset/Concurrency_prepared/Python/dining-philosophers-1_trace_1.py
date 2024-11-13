class Philosopher(threading.Thread):

    def __init__(self, xname, forkOnLeft, forkOnRight, max_steps):
        threading.Thread.__init__(self)
        self.name = xname
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight
        self.max_steps = max_steps
        self.steps_taken = 0  # Track the number of dine steps taken

    def run(self):
        while self.steps_taken < self.max_steps:
            time.sleep(random.uniform(3, 13))  # Thinking
            print(f'{self.name} is hungry.')
            self.dine()
            self.steps_taken += 1
        print(f"{self.name} has completed {self.max_steps} dining steps and stops.")

    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight

        while True:
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked:
                break
            fork1.release()
            print(f'{self.name} swaps forks')
            fork1, fork2 = fork2, fork1
        else:
            return

        self.dining()
        fork2.release()
        fork1.release()

    def dining(self):
        print(f'{self.name} starts eating ')
        time.sleep(random.uniform(1, 10))  # Eating
        print(f'{self.name} finishes eating and leaves to think.')

if __name__ == "__main__":
    philosopherNames = ('Aristotle', 'Kant')
    forks = [threading.Lock() for _ in range(len(philosopherNames))]
    max_steps = 3  # Set the desired number of dine steps per philosopher

    philosophers = [
        Philosopher(philosopherNames[i], forks[i % len(philosopherNames)], forks[(i + 1) % len(philosopherNames)], max_steps)
        for i in range(len(philosopherNames))
    ]

    for p in philosophers:
        p.start()#START

    for p in philosophers:
        p.join()#END

    print("Test finished.")
