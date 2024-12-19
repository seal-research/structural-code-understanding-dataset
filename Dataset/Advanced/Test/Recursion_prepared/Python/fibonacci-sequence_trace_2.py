def fibonacci(n):
    # Base cases: fib(0) = 0, fib(1) = 1
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    # Recursive case: fib(n) = fib(n-1) + fib(n-2)
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == "__main__":
  print(fibonacci(15))