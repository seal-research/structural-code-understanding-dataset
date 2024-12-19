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
    barrier = threading.Barrier(5)
    w1 = threading.Thread(target=worker, args=((10,barrier)))
    w2 = threading.Thread(target=worker, args=((11,barrier)))
    w3 = threading.Thread(target=worker, args=((12,barrier)))
    w4 = threading.Thread(target=worker, args=((13,barrier)))
    w5 = threading.Thread(target=worker, args=((14,barrier)))
    w1.start() #START

    w2.start()
    w3.start()
    w4.start()
    w5.start()

    w1.join()
    w2.join()
    w3.join()
    w4.join()
    w5.join()