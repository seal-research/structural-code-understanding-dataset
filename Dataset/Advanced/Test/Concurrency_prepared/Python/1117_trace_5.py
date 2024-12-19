class H2O:
    def __init__(self):
        self.h = Semaphore(2)
        self.o = Semaphore(0)

    def hydrogen(self, releaseHydrogen: "Callable[[], None]") -> None:
        self.h.acquire()
        # releaseHydrogen() outputs "H". Do not change or remove this line.
        releaseHydrogen()
        if self.h._value == 0: # semaphore value checker api
            self.o.release()

    def oxygen(self, releaseOxygen: "Callable[[], None]") -> None:
        self.o.acquire()
        # releaseOxygen() outputs "O". Do not change or remove this line.
        releaseOxygen()
        self.h.release(2)


if __name__ == "__main__":
    def releaseHydrogen():
        print("H", end="")

    def releaseOxygen():
        print("O", end="")

    h2o = H2O()
    
    # Create pairs of 2 hydrogen and 1 oxygen threads
    threads = []
    for _ in range(3):  # Adjust the range based on the number of H2O molecules desired
        # Start 2 hydrogen threads
        threads.append(threading.Thread(target=h2o.hydrogen, args=(releaseHydrogen,)))
        threads.append(threading.Thread(target=h2o.hydrogen, args=(releaseHydrogen,)))
        
        # Start 1 oxygen thread
        threads.append(threading.Thread(target=h2o.oxygen, args=(releaseOxygen,)))
    
    # Start and join threads
    for t in threads:
        t.start()#START
    for t in threads:
        t.join()