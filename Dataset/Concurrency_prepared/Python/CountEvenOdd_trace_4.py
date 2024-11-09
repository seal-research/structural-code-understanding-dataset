import threading

# Function to count even numbers
def count_even(numbers, result):
    count = sum(1 for num in numbers if num % 2 == 0)
    result.append(count)
    print(f"Count of even numbers: {count}")

# Function to count odd numbers
def count_odd(numbers, result):
    count = sum(1 for num in numbers if num % 2 != 0)
    result.append(count)
    print(f"Count of odd numbers: {count}")

if __name__ == "__main__":
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = []

    even_thread = threading.Thread(target=count_even, args=(numbers, result))
    odd_thread = threading.Thread(target=count_odd, args=(numbers, result))

    even_thread.start()
    odd_thread.start()

    even_thread.join()
    odd_thread.join()

    total_even, total_odd = result
    print(f"Total even: {total_even}, Total odd: {total_odd}")