import time
import threading

# Only 4 workers can run in the same time
sem = threading.Semaphore(4)

workers = []
running = 1


def worker():
    me = threading.currentThread()
    while 1:
        sem.acquire()
        try:
            if not running:
                break
            print(f'{me.getName()} acquired semaphore')
            time.sleep(2.0)
        finally:
            sem.release()
        time.sleep(0.01) # Let others acquire

if __name__ == "__main__":
    # Semaphore to allow only 4 concurrent workers
    sem = threading.Semaphore(2)

    # Control variable for stopping workers
    running = 1
    workers = []

    # Start 10 workers
    for i in range(12):
        t = threading.Thread(name=str(i), target=worker)
        workers.append(t)
        t.start()

    for t in workers:
        t.join() 