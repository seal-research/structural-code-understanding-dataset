import fractions
def lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0

if __name__ == "__main__":
    print(lcm(8, 9))