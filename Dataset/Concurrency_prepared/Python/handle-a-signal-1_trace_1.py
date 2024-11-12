def counter(max_steps=10):
    n = 0
    t1 = time.time()
    while n < max_steps:
        time.sleep(0.5)
        n += 1
        print(n)
    print(f'Program ran for {(time.time() - t1)} seconds.')

if __name__ == "__main__":
    max_steps = 5  # Set the desired number of steps
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(counter, max_steps=max_steps)
        future.result()  # Wait for the counter to complete