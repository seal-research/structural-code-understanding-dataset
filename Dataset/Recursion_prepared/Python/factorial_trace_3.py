def factorial(n):
    # Base case: 0! or 1! is 1
    if n <= 1:
        return 1
    # Recursive case: n! = n * (n-1)!
    else:
        return n * factorial(n - 1)if __name__ == "__main__":
n = 10
print(factorial(n))