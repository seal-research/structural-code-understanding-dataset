from time import time, sleep
from threading import Thread

class Integrator(Thread):
    'continuously integrate a function `K`, at each `interval` seconds'
    def __init__(self, K=lambda t:0, interval=1e-4):
        Thread.__init__(self)
        self.interval  = interval
        self.K   = K
        self.S   = 0.0
        self.__run = True
        self.start()

    def run(self):
        "entry point for the thread"
        interval = self.interval
        start = time()
        t0, k0 = 0, self.K(0)
        while self.__run:
            sleep(interval)
            t1 = time() - start
            k1 = self.K(t1)
            self.S += (k1 + k0)*(t1 - t0)/2.0
            t0, k0 = t1, k1

    def join(self):
        self.__run = False
        Thread.join(self)

if __name__ == "__main__":

    ai = Integrator(lambda t: tan(pi * t / 4))  # Use tan(pi*t/4) for more varied behavior
    sleep(1)  # Shorter sleep for more frequent changes
    print(ai.S)
    
    ai.K = lambda t: tan(pi * t / 2)  # Change the function to tan(pi*t/2)
    sleep(1.5)  # Longer sleep for more varied integration progress
    print(ai.S)
    
    ai.K = lambda t: 0  # Stop integration (function is now zero)
    sleep(0.5)  # Short sleep before printing the final result
    print(ai.S)