def gcd(a, b):
    # Base case: if b is 0, the gcd is a
    if b == 0:
        return a
    # Recursive case: gcd(a, b) = gcd(b, a % b)
    else:
        return gcd(b, a % b)

if __name__ == "__main__":
    print(gcd(770, 38))