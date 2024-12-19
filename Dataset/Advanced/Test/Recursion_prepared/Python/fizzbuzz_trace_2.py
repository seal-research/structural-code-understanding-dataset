def fizzbuzz(n):
    # Base case: if n is 0, stop recursion
    if n <= 0:
        return
    # Recursive call for the previous number
    fizzbuzz(n - 1)
    # Check the conditions and print the appropriate response
    if n % 3 == 0 and n % 5 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

if __name__ == "__main__":
    fizzbuzz(6)