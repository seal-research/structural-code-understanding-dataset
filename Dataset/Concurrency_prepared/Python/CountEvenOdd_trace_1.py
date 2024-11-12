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
    numbers = [11, 22, 33, 44, 55, 66, 77, 88, 99, 100]
    result = []

    even_thread = threading.Thread(target=count_even, args=(numbers, result))
    odd_thread = threading.Thread(target=count_odd, args=(numbers, result))

    even_thread.start()
    #START
    odd_thread.start()

    even_thread.join()
    odd_thread.join()
    #END

    total_even, total_odd = result
    print(f"Total even: {total_even}, Total odd: {total_odd}")