import math

def is_simple_power(x, n):
    if x < 1 or n < 2:
        return x == 1
    root = round(math.log(x, n))
    return n ** root == x