import threading

# Function to calculate factorial
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Function to calculate factorial for even numbers
def even_factorial(numbers, result):
    count = 0
    for num in numbers:
        if num % 2 == 0:
            count += factorial(num)
    result.append(count)
    print(f"Sum of factorials of even numbers: {count}")

# Function to calculate factorial for odd numbers
def odd_factorial(numbers, result):
    count = 0
    for num in numbers:
        if num % 2 != 0:
            count += factorial(num)
    result.append(count)
    print(f"Sum of factorials of odd numbers: {count}")

# Main function
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6]
    result = []

    even_thread = threading.Thread(target=even_factorial, args=(numbers, result))
    odd_thread = threading.Thread(target=odd_factorial, args=(numbers, result))

    even_thread.start()
    odd_thread.start()

    even_thread.join()
    odd_thread.join()

    total_even_factorial, total_odd_factorial = result
    print(f"Total sum of even factorials: {total_even_factorial}, Total sum of odd factorials: {total_odd_factorial}")
