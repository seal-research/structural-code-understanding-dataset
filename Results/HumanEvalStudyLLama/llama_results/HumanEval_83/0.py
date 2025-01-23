def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    total_numbers = 9 * (10 ** (n - 1))
    starts_with_one = 10 ** (n - 1)
    ends_with_one = 9 * (10 ** (n - 2)) * 9
    return starts_with_one + ends_with_one