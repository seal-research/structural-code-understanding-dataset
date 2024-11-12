def worker():
    me = threading.currentThread()
    for _ in range(5):  # Loop for a fixed number of steps
        sem.acquire()
        try:
            print(f'{me.getName()} acquired semaphore')
            time.sleep(2.0)  # Simulate work
        finally:
            sem.release()
        time.sleep(0.01)  # Let others acquire the semaphore

if __name__ == "__main__":
    # Semaphore to allow only 2 concurrent workers
    sem = threading.Semaphore(1)

    # Create and start 10 worker threads
    workers = []
    for i in range(12):
        t = threading.Thread(name=str(i), target=worker)
        workers.append(t)
        t.start() #START


    # Wait for all threads to complete
    for t in workers:
        t.join() #END


    print("All workers completed.")