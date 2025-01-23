def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    for i in range(2, a):
        if a % i == 0 and is_prime(i):
            for j in range(2, a // i):
                if (a // i) % j == 0 and is_prime(j) and is_prime(a // i // j):
                    return True
    return False