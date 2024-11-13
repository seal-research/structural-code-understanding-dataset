from time import time as current_time, sleep
from threading import Thread
from math import cos, sin, pi

class Integrator(Thread):
    'Integrates a function `K` for a fixed number of steps with an interval between each step.'
    
    def __init__(self, K=lambda t: 0, interval=1e-4, steps=10000):
        Thread.__init__(self)
        self.interval = interval
        self.K = K
        self.S = 0.0
        self.steps = steps  # Number of integration steps to run
        self.start()#START

    def run(self):
        "Entry point for the thread."
        interval = self.interval
        start = current_time()
        t0, k0 = 0, self.K(0)
        
        for _ in range(self.steps):
            sleep(interval)
            t1 = current_time() - start
            k1 = self.K(t1)
            self.S += (k1 + k0) * (t1 - t0) / 2.0
            t0, k0 = t1, k1

    def join(self):
        Thread.join(self)  # Wait for the thread to finish

if __name__ == "__main__":
    # Create two integrators with different functions
    integrator1 = Integrator(lambda t: cos(pi * t), steps=10)#START
    integrator2 = Integrator(lambda t: sin(pi * t), steps=10)

    # Wait for both integrators to complete
    integrator1.join()
    integrator2.join()#END

    # Print the results of each integrator
    print("Integrator 1 result:", integrator1.S)
    print("Integrator 2 result:", integrator2.S)
