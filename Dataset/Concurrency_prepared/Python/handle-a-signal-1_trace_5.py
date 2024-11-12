def counter(name, max_steps=10):
    n = 0
    t1 = time.time()
    while n < max_steps:
        time.sleep(0.5)
        n += 1
        print(f"Counter {name}: {n}")
    print(f'Counter {name} ran for %5.3f seconds.' % (time.time() - t1))

if __name__ == "__main__":
    max_steps = 10  # Set the desired number of steps for each counter
    num_counters = 4  # Number of counters to run concurrently

    # Run multiple counters concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(counter, max_steps=max_steps) for i in range(num_counters)] #START

        
        # Wait for all counters to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()
