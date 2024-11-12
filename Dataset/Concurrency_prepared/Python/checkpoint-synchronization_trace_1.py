def worker(workernum, barrier):
    # task 1
    sleeptime = random.random()
    print('Starting worker '+str(workernum)+" task 1, sleeptime="+str(sleeptime))
    time.sleep(sleeptime)
    print('Exiting worker'+str(workernum))
    barrier.wait()
    # task 2
    sleeptime = random.random()
    print('Starting worker '+str(workernum)+" task 2, sleeptime="+str(sleeptime))
    time.sleep(sleeptime)
    print('Exiting worker'+str(workernum))

if __name__ == "__main__":
    barrier = threading.Barrier(3)
    w1 = threading.Thread(target=worker, args=((1,barrier)))
    w2 = threading.Thread(target=worker, args=((2,barrier)))
    w1.start()
    #START
    w2.start()