import __main__, os

def isOnlyInstance():
    return os.system("(( $(ps -ef | grep python | grep '[" +
                     __main__.__file__[0] + "]" + __main__.__file__[1:] +
                     "' | wc -l) > 1 ))") != 0

def check_instance_periodically(steps, interval=2):
    for _ in range(steps):
        only_instance = isOnlyInstance()
        print("Is only instance:", only_instance)
        time.sleep(interval)  # Check every `interval` seconds
    print("Finished checking for other instances.")

if __name__ == "__main__":
    steps = 6  # Set the number of steps to perform the check
    interval = 6  # Set the time interval between checks in seconds

    # Start a background thread to periodically check for other instances
    checker_thread = threading.Thread(target=check_instance_periodically, args=(steps, interval))
    checker_thread.start()
    #START

    checker_thread2 = threading.Thread(target=check_instance_periodically, args=(steps, interval))
    checker_thread2.start()

    # Main thread can perform other tasks concurrently for the same number of steps
    for i in range(steps):
        print("Main thread doing other work... Step", i+1)
        time.sleep(interval)

    checker_thread.join()
    checker_thread2.join()
    #END
    print("Main program completed.")
