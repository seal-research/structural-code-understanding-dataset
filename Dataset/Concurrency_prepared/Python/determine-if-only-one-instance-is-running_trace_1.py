import __main__

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
    steps = 5  # Set the number of steps to perform the check
    interval = 2  # Set the time interval between checks in seconds

    # Start a background thread to periodically check for other instances
    checker_thread = threading.Thread(target=check_instance_periodically, args=(steps, interval))
    checker_thread.start()
    #START

    # Main thread can perform other tasks concurrently for the same number of steps
    for i in range(steps):
        print("Main thread doing other work... Step", i+1)
        time.sleep(interval)

    checker_thread.join()  # Wait for checker thread to finish
    print("Main program completed.")
