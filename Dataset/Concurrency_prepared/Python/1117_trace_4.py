from threading import Semaphore


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
    import threading
    import time

    def releaseHydrogen():
        print("H", end="")

    def releaseOxygen():
        print("O", end="")

    h2o = H2O()

    threads = []
    for _ in range(8):
        threads.append(threading.Thread(target=h2o.hydrogen, args=(releaseHydrogen,)))
    for _ in range(4):
        threads.append(threading.Thread(target=h2o.oxygen, args=(releaseOxygen,)))

    for t in threads:
        t.start()
        #START
    for t in threads:
        t.join()